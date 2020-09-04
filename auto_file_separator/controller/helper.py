import os
from os import listdir
from os.path import isfile, join

from watchdog.events import FileSystemEventHandler

from auto_file_separator.cmd.cmd import CMD


class FileSystemInitializer:

    def __init__(self):
        self.config = CMD().get_config()
        self.watch_directory = self.config["locations"]["target"]
        self.categories_locations = self.config["locations"]["div-directories"]
        self.logger = CMD().get_logger()

    def initialise_categorical_directories(self):
        divide_directories = self.categories_locations.split("|")
        divide_directories.append("default")

        for divide_directory in divide_directories:
            if divide_directory != "default":
                divide_directory_path = self.config["output-locations"][divide_directory]
            else:
                divide_directory_path = f"{self.watch_directory}\\default"

            if not os.path.isdir(divide_directory_path):
                os.mkdir(divide_directory_path)
                self.logger.warning(f"Successfully created the directory: {divide_directory_path}")
            else:
                self.logger.info(f"Skipping creation of folder: {divide_directory_path}")

    def initialise_target_directory(self):
        if os.path.isdir(f"{self.watch_directory}"):
            self.logger.info(f"Skipping creation of folder: 👉 {self.watch_directory} 👈")
        else:
            self.logger.info(f"Target Folder Not Exists !")
            try:
                os.mkdir(self.watch_directory)
            except OSError:
                self.logger.warning(f"Creation of the Target Directory {self.watch_directory} failed !")
            else:
                self.logger.info(f"Successfully created the Target Directory {self.watch_directory}")


class Handler(FileSystemEventHandler):
    @staticmethod
    def on_any_event(event):
        logger = CMD().get_logger()
        if event.is_directory:
            return None
        elif event.event_type == "deleted":
            # Event is modified, you can process it now
            logger.info(f"Watchdog received {event.event_type} event - {event.src_path}")
        elif event.event_type != "deleted":
            # Event is created, you can process it now
            distributionMaster = DistributionMaster()
            distributionMaster.distribution_controller()
            logger.info(f"Watchdog received {event.event_type} event - {event.src_path}.")


class DistributionMaster:
    def __init__(self):
        self.target_path = CMD().get_config()["locations"]["target"]
        self.files = list()
        self.extensions = CMD().get_extensions_list()

    def distribution_controller(self):
        self.files = [file for file in listdir(self.target_path) if isfile(join(self.target_path, file))]
        for file in self.files:
            self.move_file_by_extension_type(file)
            break

    def move_file_by_extension_type(self, file):
        match, folder_location = False, ""
        filepath = f"{self.target_path}\\{file}"
        for extension_type, extension in self.extensions.items():
            current_file_extension = file.split('.')[-1]
            if current_file_extension in extension:
                match, folder_location = True, extension_type

        if match:
            location = f'{self.target_path}\\{folder_location}'
        else:
            location = f"{self.target_path}\\default"
        CMD().move_file_to_folder(filepath=filepath, location=location)

