import time

from watchdog.observers import Observer

from auto_file_separator.cmd.cmd import CMD
from auto_file_separator.controller.helper import FileSystemInitializer, Handler


class DirectoryWatchController:
    def __init__(self):
        # getting the location of target directory
        self.watch_directory = CMD().get_config()["locations"]["target"]
        # getting the logger object
        self.logger = CMD().get_logger()
        # getting a `watchdog` Observer object
        self.observer = Observer()
        # getting `FileSystemInitializer` object
        self.fileSystemInitializer = FileSystemInitializer()

    def run(self):
        """
        Function which controls and manages the files of Target Directory
        :return: None
        """
        # initializes the target directory
        self.fileSystemInitializer.initialise_target_directory()
        # initializer the categories' directories
        self.fileSystemInitializer.initialise_categorical_directories()
        # creating the event handler
        event_handler = Handler()

        # scheduling the observer object
        self.observer.schedule(event_handler, self.watch_directory, recursive=True)
        # starting the observer object
        self.observer.start()

        try:
            while True:
                # TOS = 5 seconds
                time.sleep(5)
        except Exception:
            # Stops the execution
            self.observer.stop()
            self.logger.info("Observer Stopped !")
        self.observer.join()





