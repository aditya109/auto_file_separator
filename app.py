import configparser
import shutil
import json
import logging
import os
import pprint
import time
import yaml
from os import path, listdir
from os.path import isfile, join
from watchdog.events import LoggingEventHandler, FileSystemEventHandler
from watchdog.observers import Observer

config = configparser.ConfigParser()
config.read("./config.ini")

with open("extensions.json", "r") as json_file:
    extensions_json = json.loads(json_file.readline())
    with open('config.yaml', 'w') as config_yaml_file:
        yaml.dump(extensions_json, config_yaml_file, default_flow_style=False)

pp = pprint.PrettyPrinter(indent=4)


class DistributionMaster:
    path = config["locations"]["target"]

    def __init__(self):
        self.files = list()

    def distribution_controller(self):
        self.files = [file for file in listdir(self.path) if isfile(join(self.path, file))]
        for file in self.files:
            self.identify_file_type(file)

    @staticmethod
    def identify_file_type(file):
        match, folder_location = False, ""
        for type, ext in extensions_json.items():
            current_file_extension = f".{file.split('.')[-1]}"
            if current_file_extension in ext:
                match, folder_location = True, type

        if match:
            path = f'{config["locations"]["target"]}\\{folder_location}'
            move_file_to_folder(file=file, location=path)
        else:
            path = f'{config["locations"]["target"]}\\default'
            move_file_to_folder(file=file, location=path)


def move_file_to_folder(file, location):
    file_path = f"{config['locations']['target']}\\{file}"
    shutil.move(file_path, location)


class OnMyWatch:
    # Set the directory on watch
    watch_directory = config["locations"]["target"]

    def __init__(self):
        self.observer = Observer()

    def initialise_categorical_directories(self):
        divide_directories = (config["locations"]["div-directories"]).split("|")
        divide_directories.append("default")

        for directory in divide_directories:
            if directory != "default":
                path = config["output-locations"][directory]
            else:
                path = f"{self.watch_directory}\\default"

            if not os.path.isdir(path):
                os.mkdir(path)
                logging.warning(f"Successfully created the directory: {path}")
            else:
                logging.info(f"Skipping creation of folder: {path}")

    def initialise_target_directory(self):
        if os.path.isdir(f"{self.watch_directory}"):
            logging.info(f"Skipping creation of folder: 👉 {self.watch_directory} 👈")
        else:
            logging.info(f"Target Folder Not Exists !")
            try:
                os.mkdir(self.watch_directory)
            except OSError:
                logging.warning(f"Creation of the Target Directory {self.watch_directory} failed !")
            else:
                logging.info(f"Successfully created the Target Directory {self.watch_directory}")

    def run(self):
        self.initialise_target_directory()
        self.initialise_categorical_directories()
        event_handler = Handler()
        self.observer.schedule(event_handler, self.watch_directory, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except Exception:
            self.observer.stop()
            print("Observer Stopped")
        self.observer.join()


class Handler(FileSystemEventHandler):
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None
        elif event.event_type == "deleted":
            # Event is modified, you can process it now
            logging.info(f"Watchdog received {event.event_type} event - {event.src_path}")
        elif event.event_type != "deleted":
            # Event is created, you can process it now
            logging.info(f"Watchdog received {event.event_type} event - {event.src_path}.")


def read_extensions():
    with open("extensions.json", "r") as file:
        data = json.load(file)
    return data


if __name__ == "__main__":
    obj = DistributionMaster()
    obj.distribution_controller()
    # watch = OnMyWatch()
    # watch.run()
