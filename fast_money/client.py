#!/usr/bin/python3
import pathlib
import tkinter as tk
import pygubu
from clientui import ClientUI


class Client(ClientUI):
    def __init__(self, master=None):
        super().__init__(master)

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
    app = Client()
    app.run()
