import time

from watchdog.observers import Observer

from auto_file_separator.cmd.cmd import CMD
from auto_file_separator.controller.helper import FileSystemInitializer, Handler


class DirectoryWatchController:
    def __init__(self):
        self.watch_directory = CMD().get_config()["locations"]["target"]
        self.logger = CMD().get_logger()
        self.observer = Observer()
        self.fileSystemInitializer = FileSystemInitializer()

    def run(self):
        self.fileSystemInitializer.initialise_target_directory()
        self.fileSystemInitializer.initialise_categorical_directories()
        event_handler = Handler()

        self.observer.schedule(event_handler, self.watch_directory, recursive=True)
        self.observer.start()

        try:
            while True:
                time.sleep(5)
        except Exception:
            self.observer.stop()
            self.logger.info("Observer Stopped !")
        self.observer.join()





