
import logging
from config import Config


class LoggerWrapper:

    def __init__(self, config:Config):

        logs_file_path = config.file_paths["logs"]["logs"]

        # Créer un logger
        self.logger = logging.getLogger("doctolib_logger")
        self.logger.setLevel(logging.DEBUG)  # Niveau global du logger

        # Formatter : détermine la façon dont les messages seront affichés
        formatter = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s')

        # Handler pour la console
        console_handler = logging.StreamHandler()
        console_handler.setLevel(config.logger_config["console"]["level"])  # Niveau de log pour la console
        console_handler.setFormatter(formatter)

        # Handler pour le fichier
        file_handler = logging.FileHandler(logs_file_path)
        file_handler.setLevel(config.logger_config["file"]["level"])  # Niveau de log pour le fichier
        file_handler.setFormatter(formatter)

        # Ajouter les handlers au logger
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)

        self.logger.info("Logging Started")

        self.debug = self.logger.debug
        self.info = self.logger.info
        self.error = self.logger.error
        self.exception = self.logger.exception


    def end_logging(self):
        self.logger.info("Program Finished")


    def fun_with_log(self, fun):
        def wrapper(*args, **kargs):
            self.logger.info(f"Function call \"{fun.__name__}\" with args : {args}, and kargs : {kargs}")
            result = fun(*args, **kargs)
            return result
        return wrapper