import os
from os import listdir
from os.path import isfile, join

from watchdog.events import FileSystemEventHandler

from auto_file_separator.cmd.cmd import CMD


class FileSystemInitializer:
    """
    Initializes the related directories
    """

    def __init__(self):
        # getting config as a dictionary
        self.config = CMD().get_config()
        # setting the target directory as a watch directory
        self.watch_directory = self.config["locations"]["target"]
        # setting the categorical directories
        self.categories_locations = self.config["locations"]["div-directories"]
        # getting the logger object
        self.logger = CMD().get_logger()

    def initialise_categorical_directories(self):
        """
        Checks the existence of categorical directories, creates such directory paths as and when required
        :return: None
        """
        # getting the names of the directories
        divide_directories = self.categories_locations.split("|")
        # appending `default` directory for those files which do not match at all
        divide_directories.append("default")

        # iterating through the names of all categorical directories
        for divide_directory in divide_directories:
            # making the paths for checking or creation
            if divide_directory != "default":
                divide_directory_path = self.config["output-locations"][divide_directory]
            else:
                divide_directory_path = f"{self.watch_directory}\\default"

            # checking for non-existence of the directory
            if not os.path.isdir(divide_directory_path):
                # makes the directory
                os.mkdir(divide_directory_path)
                self.logger.warning(f"Successfully created the directory: {divide_directory_path}")
            else:
                # skips if it already exists
                self.logger.info(f"Skipping creation of folder: {divide_directory_path}")

    def initialise_target_directory(self):
        """
        Checks the existence of target Directory, creates such directory paths as and when required
        :return: boolean
        """
        # checks the existence of the target directory
        if os.path.isdir(f"{self.watch_directory}"):
            self.logger.info(f"Skipping creation of folder: 👉 {self.watch_directory} 👈")
        else:
            self.logger.info(f"Target Folder Not Exists !")
            try:
                # creates the target directory if the directory does not exists
                os.mkdir(self.watch_directory)
            except OSError:
                self.logger.warning(f"Creation of the Target Directory {self.watch_directory} failed !")
                return False
            else:
                self.logger.info(f"Successfully created the Target Directory {self.watch_directory}")
        return True


class Handler(FileSystemEventHandler):
    """
    Creates a FileSystemEventHandler
    """
    @staticmethod
    def on_any_event(event):
        """
        Describes the flow on file system events
        :param event:class:`FileSystemEvent`
        :return: None
        """
        # getting a logger object
        logger = CMD().get_logger()
        if event.is_directory:
            return None
        elif event.event_type == "deleted":
            # Event is deleted, you can process it now
            logger.info(f"Watchdog received {event.event_type} event - {event.src_path}")
        elif event.event_type != "deleted":
            # Event is created, modified, moved, you can process it now
            # creating a DistributionMaster object
            distributionMaster = DistributionMaster()
            # calls the controller for file distribution
            distributionMaster.distribution_controller()
            logger.info(f"Watchdog received {event.event_type} event - {event.src_path}.")


class DistributionMaster:
    """
    Controls the files distribution of the files of the target directory
    """
    def __init__(self):
        # getting the config as a dictionary
        self.target_path = CMD().get_config()["locations"]["target"]
        # initializing the list for storing the files
        self.files = list()
        # getting the extensions from static yaml
        self.extensions = CMD().get_extensions_list()

    def distribution_controller(self):
        """
        Distributes the files according to the extensions
        :return: None
        """
        # grabbing the files in the target directory
        self.files = [file for file in listdir(self.target_path) if isfile(join(self.target_path, file))]
        # iterating the files in the files' list
        for file in self.files:
            # move the file by extension type
            self.move_file_by_extension_type(file)

    def move_file_by_extension_type(self, file):
        """
        Moves the files on the basis of the extensions
        :param file: string
        :return: None
        """
        # creating the flag to indicate match and folder_location
        match, folder_location = False, ""
        filepath = f"{self.target_path}\\{file}"
        # iterating the through all the extensions received from the static yaml
        for extension_type, extension in self.extensions.items():
            current_file_extension = file.split('.')[-1]
            if current_file_extension in extension:
                match, folder_location = True, extension_type
        # moves the file to the specified location when the match is found
        if match:
            location = f'{self.target_path}\\{folder_location}'
        else:
            #  moves the file to the specified location when the match is not found
            location = f"{self.target_path}\\default"
        # initiated the move of the file to location
        CMD().move_file_to_folder(filepath=filepath, location=location)

