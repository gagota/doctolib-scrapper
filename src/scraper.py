# Public Libraries
import traceback, json
from playwright.sync_api import sync_playwright
from playwright.sync_api import Page, Playwright, Browser, BrowserContext
from urllib.parse import urlparse, ParseResult
from bs4 import BeautifulSoup, Tag

# Custom Libraries
from logger_wrapper import LoggerWrapper
from data_manager import save_data
from config import Config



class ScraperLogger:

    def __init__(self, logger:LoggerWrapper):
        self.logger = logger

    def loggify_page(self, page:Page):

        def loggify_goto(fun_goto):
            def wrapper(*args, **kargs):
                url = args[0]
                self.logger.info(f"Going to site : {url}")
                return fun_goto(*args, **kargs)
            return wrapper

        page.goto = loggify_goto(page.goto)

        return page



class Scraper:

    def __init__(self, logger:LoggerWrapper, headless = True):
        logger.debug("scrapper init")

        self.headless = headless
        self.logger = logger
        self.scraper_logger = ScraperLogger(logger)
        
        self.playwright:Playwright = None
        self.browser:Browser = None
        self.bs_context:BrowserContext = None
        self.page:Page = None

        self.domains_list:list[str] = []


#region Utils
    def init_new_domain(self, new_domain:str):
        """
        Sometimes you need to refuse cookies the first time you
        enter the site when you have a blank brower context
        """
        self.domains_list.append(new_domain)


    def check_new_domain(self, url:str):
        parsed_url:ParseResult = urlparse(url)
        domain:str = parsed_url.netloc  # extrait le nom de domaine
        if not domain in self.domains_list:
            self.init_new_domain(domain)


    def renew_context(self):
        self.logger.debug("renew_context : current_url = self.page.url")
        current_url = self.page.url
        self.logger.debug("renew_context : self.bs_context = self.browser.new_context()")
        self.bs_context = self.browser.new_context()
        self.logger.debug("renew_context : self.page.close()")
        self.page.close()

        self.logger.debug("renew_context : self.page = self.bs_context.new_page()")
        self.page = self.bs_context.new_page()
        self.logger.debug("renew_context : self.page.goto(current_url)")
        self.page.goto(current_url)

        self.logger.info("Browser Context renewed")
#endregion


#region Wrappers
    def wrap_page(self, page:Page):
        # Go To
        def wrap_goto(goto_fun):
            self.logger.debug("wrapper created for : page.goto()")
            def wrapper(*args, **kargs):
                goto_fun(*args, **kargs)

                url = args[0]
                self.check_new_domain(url)

            return wrapper
        
        page = self.scraper_logger.loggify_page(page)
        page.goto = wrap_goto(page.goto)

        return page


    def wrap_context(self, bs_context:BrowserContext):
        # New Page
        def init_new_page(new_page:Page):
            new_page = self.wrap_page(new_page)
            return new_page

        def wrap_fun_new_page(new_page_fun):
            self.logger.debug("wrapper created for : bs_context.new_page()")
            def wrapper(*args, **kargs):
                new_page = new_page_fun(*args, **kargs)
                new_page = init_new_page(new_page)
                return new_page
            return wrapper
        
        bs_context.new_page = wrap_fun_new_page(bs_context.new_page)
        return bs_context


    def wrap_browser(self, browser:Browser):
        """We add some extra behaviors for when a new page is created

        Args:
            browser (Browser): Browser to add the behaviors
        """

        # New Context
        def wrap_fun_new_context(new_context_fun):
            self.logger.debug("wrapper created for : browser.new_context()")
            def wrapper(*args, **kargs):
                new_context = new_context_fun(*args, **kargs)
                assert(isinstance(new_context, BrowserContext))

                new_context = self.wrap_context(new_context)

                # We empty the list of domains
                self.domains_list = []

                return new_context
            return wrapper
        
        browser.new_context = wrap_fun_new_context(browser.new_context)

        def wrap_fun_new_page():
            self.logger.debug("wrapper created for : browser.new_page()")
            def wrapper(*args, **kargs):
                # We want to create a new context to do it properly
                self.bs_context = browser.new_context()
                return self.bs_context.new_page(*args, **kargs)
            return wrapper

        browser.new_page = wrap_fun_new_page()

        return browser
#endregion


#region Enter / Exit (to use `with Scraper`)
    def __enter__(self):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=self.headless)
        self.browser = self.wrap_browser(self.browser)
        self.bs_context = self.browser.new_context()
        self.page = self.bs_context.new_page()

        self.logger.info("Scraper Entered")
        return self
    

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.browser.close()
        self.playwright.stop()

        self.logger.info("Scraper Exited")
#endregion



class DoctolibScraper(Scraper):

    #region Utils    
    def json_from_html(self, html:str):
        soup = BeautifulSoup(html, features="lxml")
        pre = soup.find("pre")
        data = json.loads(pre.get_text())
        return data
    #endregion
    

    def __init__(self, config:Config, logger:LoggerWrapper):
        self.file_paths = config.file_paths
        super().__init__(logger, config.headless_scrap)

        self.doctolib_search_url = config.doctolib_search_url
        self.data_subfolder = config.subfolder_name
        self.config = config
        self.logger = logger


    #region Doctors Links
    def find_docs_links(self, data:list):
        docs_links = []
        for doc_infos in data:
            link = "https://www.doctolib.fr" + doc_infos["link"]
            docs_links.append(link)
        return docs_links


    def gather_doctors_links(self, save:bool=True)->list:
        docs_links = []
        for i in range(1, 1000):
            if i==1:
                self.page.goto(self.doctolib_search_url + ".json") #"page=1" doesn't work for some reason
            else:
                self.page.goto(self.doctolib_search_url + f".json?page={i}")
            
            current_data = self.json_from_html(self.page.content())["data"]
            docs_infos = current_data["doctors"]

            if len(docs_infos) == 0:
                break
            else:
                docs_links += self.find_docs_links(docs_infos)
        
        #We remove doublons
        docs_links = list(set(docs_links))

        if save:
            save_data(docs_links, self.file_paths["data"]["docs_links"])

        return docs_links
    #endregion


    #region Doctors Infos
    def find_doc_infos(self, doc_url:str)->dict:
        self.logger.info(f"find_doc_infos, doc_url : {doc_url}")

        week_days = {
            1:"Lun",
            2:"Mar",
            3:"Mer",
            4:"Jeu",
            5:"Ven",
            6:"Sam",
            7:"Dim",
        }
        nb_try_max = 3
        for i in range(nb_try_max):
            self.logger.info(f"try {i}...")
            try:
                doc_infos = {}
                
                self.page.goto(doc_url + ".json")
                self.page.wait_for_load_state("domcontentloaded")

                data = self.json_from_html(self.page.content())["data"]

                # Page Link
                doc_infos["page_link"] = doc_url

                # Name
                doc_infos["doctor_name"] = data["profile"]["name_with_title"]

                # Image
                image_id = data["profile"]["avatar_picture"]["public_id"]
                doc_infos["image_link"] = f"https://media.doctolib.com/image/upload/q_auto:eco,f_auto,w_120,h_120,c_fill,g_face/{image_id}.jpg"

                # Address
                doc_infos["address"] = data["places"][0]["full_address"]

                #region Opening Hours
                opening_hours_list = []
                opening_hours_data = data["places"][0].get("opening_hours")
                if opening_hours_data == None:
                    doc_infos["opening_hours"] = None
                else:
                    for day_open_hours in data["places"][0]["opening_hours"]:
                        day = week_days[day_open_hours["day"]]

                        hour_ranges_list = []
                        for hour_range in day_open_hours["ranges"]:
                            hour_range_text = " - ".join(hour_range).replace(":", "h")
                            hour_ranges_list.append(hour_range_text)
                        hour_ranges_text = ", ".join(hour_ranges_list)

                        day_open_hours_text = day + " : " + hour_ranges_text
                        opening_hours_list.append(day_open_hours_text)
                    opening_hours_text = "\n".join(opening_hours_list)
                    doc_infos["opening_hours"] = opening_hours_text
                #endregion

                #region Tarifs
                fees = data["fees"]
                fees_texts_list = []
                for fee in fees:
                    fee_name = fee["name"]
                    min_price = fee["min_price"]
                    max_price = fee["max_price"]
                    if max_price == None:
                        text = f"{fee_name} : {min_price}€"
                    else:
                        text = f"{fee_name} : {min_price}€ - {max_price}€"
                    fees_texts_list.append(text)
                doc_infos["fees"] = "\n".join(fees_texts_list)
                #endregion

                # Phone number
                doc_infos["phone_number"] = data["places"][0].get("landline_number")

                self.logger.info("Success !")
                # Everything went right, so we break out of the loop
                break

            except Exception as e:
                self.logger.info("Failure.")
                self.logger.exception(e)
                print(traceback.print_exception(e))

                def save_html():
                    with open(self.file_paths["logs"]["last_html_page"], "w", encoding="utf-8") as f:
                        soup = BeautifulSoup(self.page.content(), "html.parser")
                        text = soup.decode(pretty_print=True)
                        f.write(text)
                    self.logger.info("HTML saved")
                save_html()

                # self.page.pause()

                self.renew_context()


        return doc_infos


    def find_docs_infos(self, docs_links:list, save:bool=True)->list:
        docs_infos = []

        # "limit_scrapping" limits the scrapping to only 5 doctors. Used for testing
        limit_scrapping = self.config.limit_scrapping
        if limit_scrapping :
            i = 0
            max_docs = 5

        try:
            for doc_link in docs_links:
                doc_infos = self.find_doc_infos(doc_link)
                docs_infos.append(doc_infos)

                # We stop the scrapping if limit_scrapping==true and we processed 5 doctors
                if limit_scrapping:
                    i += 1
                    if i >= max_docs:
                        break
        finally:
            # We backup the progress made, even if something went wrong
            if save:
                save_data(docs_infos, self.file_paths["data"]["docs_infos"])

        return docs_infos
    #endregion
