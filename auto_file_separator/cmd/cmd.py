import configparser
import logging
import logging.config
import pprint
import shutil
from os import path

import rootpath
import yaml

pp = pprint.PrettyPrinter(indent=4)


class CMD:

    def __init__(self):
        self.path = rootpath.detect()
        logging.config.fileConfig(fname=f"{self.path}\\data\\log.conf")
        self.logger = logging.getLogger('dev')
        self.config = configparser.ConfigParser()
        self.config.read(f'{self.path}\\data\\default_config.ini')

    def move_file_to_folder(self, filepath, location):
        """
        Function moves file on filepath to location
        :param filepath: string
        :param location: string
        :return: boolean
        """

        # getting the logger object
        logger = self.get_logger()
        # checking if the location exists
        if not path.exists(location):
            logger.error(f"{location} does not exist")
            # returning False if the location does not exist
            return False
        else:
            # checking if the file exists
            if not path.isfile(filepath):
                logger.error(f"{filepath} does not exist")
                # returning False if the file does not exist
                return False
            else:
                # moving file to location using shutil
                shutil.move(filepath, location)
                logger.info(f"Move successful : {filepath} to {location}")
                # returning True
                return True

    def get_config(self):
        """
        Function returns config file as a dictionary
        :return: dict
        """
        return self.config

    def get_extensions_list(self):
        """
        Function returns dictionary of extensions, reading it from the yaml file
        :return: dict
        """
        with open(f'{self.path}\\data\\default_extensions.yml', 'r') as config_yaml_file:
            default_extensions = yaml.load(config_yaml_file, Loader=yaml.FullLoader)
            return default_extensions

    def get_logger(self):
        """
        Function return a configured logger object
        :return: Logger
        """
        return self.logger

    def get_root_path(self):
        """
        Function returns the root project directory path
        :return: string
        """
        return self.path
