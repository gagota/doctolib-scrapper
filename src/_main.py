from config import Config, Parameters, Input
from data_manager import load_data
from scraper import DoctolibScraper
from logger_wrapper import LoggerWrapper





input = Input(
    home_adress = "55 rue du Faubourg-Saint-Honoré 75008 Paris", #Your adress
    doctolib_search_url = "https://www.doctolib.fr/medecin-generaliste/paris", #Url to your search
    search_name = "médecin_généraliste", #Your search name
)

parameters = Parameters(
    limit_scrapping = False,
    headless_scrap=False,
    do_steps = {
        "gather_doctors_links": True,
        "find_docs_infos": True,
    }
)



def main():
    # - Init Config -
    config = Config(
        input = input,
        parameters = parameters
    )
    
    # - Init Logging -
    logger = LoggerWrapper(config)

    do_steps = config.do_steps
    try:
        # - Scrapping -
        if do_steps["gather_doctors_links"] or do_steps["find_docs_infos"]:
            with DoctolibScraper(config, logger) as scraper:

                # Doctors links
                if do_steps["gather_doctors_links"]:
                    docs_links = scraper.gather_doctors_links()
                else:
                    docs_links = load_data(config.file_paths["data"]["docs_links"])

                # Doctors infos
                if do_steps["find_docs_infos"]:
                    scraper.find_docs_infos(docs_links)

    
    except Exception as e:
        logger.exception(e)

    logger.end_logging()
    

if __name__ == "__main__":
    main()
