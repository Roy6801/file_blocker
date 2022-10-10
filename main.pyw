from watcher import get_observer
from hotkey import HotkeyListener
from tkinter import *
from queue import Queue
from dotenv import find_dotenv, load_dotenv
import time
import os

load_dotenv(find_dotenv())


def auth_window(watcher):
    window = Tk()
    window.minsize(300, 300)
    window.maxsize(300, 300)
    window.title("Auth Panel")
    window.protocol("WM_DELETE_WINDOW", lambda: None)
    window.wm_attributes("-topmost", True)

    def clicked():
        if pwd_field.get().strip() == os.getenv("pwd"):
            watcher.stop()
            window.destroy()

    Label(window, text="Password",
          font=("Arial Bold", 24)).place(relx=.5, rely=.3, anchor=CENTER)
    pwd_field = Entry(window, width=25)
    pwd_field.place(relx=.5, rely=.5, anchor=CENTER)
    Button(window, text="Authorize", command=clicked).place(relx=.7,
                                                            rely=.8,
                                                            anchor=CENTER)

    window.withdraw()
    return window


if __name__ == "__main__":
    observer = get_observer()
    window = auth_window(watcher=observer)
    win_cmd = Queue(maxsize=1)
    listener = HotkeyListener(win_cmd=win_cmd)
    listener.start()
    observer.start()
    interval = 1.0
    try:
        while observer.is_alive():
            # print(win_cmd.qsize())
            if win_cmd.full():
                win_show = win_cmd.get()
                # print(win_show)
                if win_show:
                    interval = 0.1
                    window.deiconify()
                else:
                    interval = 1.0
                    window.withdraw()
            window.update()
            time.sleep(interval)
    finally:
        observer.stop()
        observer.join()
        listener.stop()
        listener.join()
