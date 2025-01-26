import os, time, logging



class Input:
    # Variables that have to be specified
    def __init__(
        self,
        home_adress:str,
        doctolib_search_url:str,
        search_name:str,
    ):
        self.home_adress = home_adress
        self.doctolib_search_url = doctolib_search_url
        self.search_name = search_name


class Parameters:
    # Variables that can be modified
    def __init__(
        self,
        limit_scrapping:bool = True,
        logger_config:dict = {
            "console": {"level": logging.DEBUG},
            "file": {"level": logging.DEBUG},
        },
        subfolder_name:str = None,
        do_steps:dict = {
            "gather_doctors_links": False,
            "find_docs_infos": False,
        },
        headless_scrap:bool = True,
    ):
        self.limit_scrapping = limit_scrapping
        self.logger_config = logger_config
        self.subfolder_name = subfolder_name
        self.do_steps = do_steps
        self.headless_scrap = headless_scrap


class FilePathMaker:

    def make_logs_file_path()->list:
        logs_folder = "logs"
        
        folder_year = time.strftime("%Y")
        folder_mounth = time.strftime("%m")
        folder_day = time.strftime("%d")
        current_date_time = time.strftime("%Y-%m-%d_%H-%M-%S")
        logs_file_name = f"logs_{current_date_time}.txt"

        logs_file_path = [
            logs_folder,
            folder_year, folder_mounth, folder_day,
            logs_file_name
        ]

        return logs_file_path


    def check_path_existance(file_path:str):
        folder_path = os.path.dirname(file_path)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)


    def make_file_paths_from_template(file_paths_template:dict)->dict:
        file_paths = {}
        cur_wd = os.path.dirname(__file__)

        for category, paths in file_paths_template.items():
            file_paths[category] = {}

            assert(isinstance(paths, dict))
            for path_name, folder_list in paths.items():
                file_paths[category][path_name] = os.path.join(cur_wd, *folder_list)

                FilePathMaker.check_path_existance(file_paths[category][path_name])
    
        return file_paths


class Config:
    def __init__(
        self,
        input:Input,
        parameters:Parameters = Parameters(),
    ):
        # Input
        self.home_adress = input.home_adress
        self.doctolib_search_url = input.doctolib_search_url
        self.search_name = input.search_name
        
        # Parameters
        self.limit_scrapping = parameters.limit_scrapping
        self.logger_config = parameters.logger_config
        self.do_steps = parameters.do_steps
        self.headless_scrap = parameters.headless_scrap
        # Constructed
        self.subfolder_name = parameters.subfolder_name if parameters.subfolder_name != None else input.search_name

        # File Paths
        # The template is easier to read and fill than the actual "paths_list" plain definition
        file_paths_template = {
            "data":{
                "docs_links": ["data", self.subfolder_name, "doctors_links.yaml"],
                "docs_infos": ["data", self.subfolder_name, "doctors_informations.yaml"],
            },
            "logs":{
                "logs": FilePathMaker.make_logs_file_path(),
                "last_html_page": ["logs", "last_page.html"],
                "scrapper_steps_made": ["logs", self.subfolder_name, "scrapper_steps_made.yaml"],
            },
        }
        self.file_paths:dict = FilePathMaker.make_file_paths_from_template(file_paths_template)