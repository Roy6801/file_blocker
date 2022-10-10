from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from win32api import GetLogicalDriveStrings
from win32file import GetDriveType, DRIVE_FIXED
from dotenv import find_dotenv, load_dotenv
from threading import Thread
import time
import os

load_dotenv(find_dotenv())
user = os.getenv("user")


class Watcher(PatternMatchingEventHandler):

    def __init__(self, observer, file_types=None):
        super().__init__(patterns=file_types)
        self.failed = set()
        self.observer = observer
        self.retry = Thread(target=self.retry_remove)
        self.retry.start()

    def on_created(self, event):
        time.sleep(0.5)
        try:
            os.remove(event.src_path)
        except Exception as e:
            print(e)
            self.failed.add(event.src_path)

    def retry_remove(self):
        time.sleep(10.0)
        while self.observer.is_alive():
            if len(self.failed) > 0:
                for file in self.failed:
                    try:
                        os.remove(file)
                    except Exception as e:
                        print(e)
            time.sleep(5.0)


def getAllDrives():
    drives = GetLogicalDriveStrings()
    drives = drives.split('\000')[:-1]
    drives = [drive for drive in drives if GetDriveType(drive) == DRIVE_FIXED]
    drives.remove("C:\\")
    for dir in ["Downloads", "Desktop"]:
        drives.append(f"{user}\{dir}")
    return drives


def get_observer():
    paths = getAllDrives()
    # print(paths)

    observer = Observer()
    event_handler = Watcher(observer,
                            file_types=["*.exe", "*.rar", "*.zip", "*.7z"])

    for path in paths:
        observer.schedule(event_handler, path, recursive=True)
    return observer
