from pynput import keyboard
from pynput.keyboard import Key

combo = set()
keys = {Key.space, Key.up, Key.down}
cmbs = ({Key.space, Key.up}, {Key.space, Key.down})


class HotkeyListener(keyboard.Listener):

    def __init__(self, win_cmd):
        super().__init__(on_press=self.on_press, on_release=self.on_release)
        self.cmd = win_cmd

    def on_press(self, key):
        if key in keys: combo.add(key)

        if combo == cmbs[0]:
            self.open_auth()
        elif combo == cmbs[1]:
            self.close_auth()

    def on_release(self, key):
        if key in combo: combo.remove(key)

    def open_auth(self):
        self.cmd.put(True)

    def close_auth(self):
        self.cmd.put(False)
