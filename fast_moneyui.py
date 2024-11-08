#!/usr/bin/python3
import pathlib
import tkinter as tk
import pygubu

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "FastMoneyClient.ui"
RESOURCE_PATHS = [PROJECT_PATH]


class FastMoneyClientUI:
    def __init__(self, master=None):
        self.builder = pygubu.Builder()
        self.builder.add_resource_paths(RESOURCE_PATHS)
        self.builder.add_from_file(PROJECT_UI)
        # Main widget
        self.mainwindow: tk.Tk = self.builder.get_object("root", master)
        self.builder.connect_callbacks(self)

    def run(self):
        self.mainwindow.mainloop()

    def connect_to_server(self):
        pass

    def set_timer_duration(self):
        pass

    def start_timer(self):
        pass

    def play_duplicate_sound(self):
        pass

    def commit(self):
        pass


if __name__ == "__main__":
    app = FastMoneyClientUI()
    app.run()
