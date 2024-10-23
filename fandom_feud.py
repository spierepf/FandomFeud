#!/usr/bin/python3
import pathlib
import tkinter as tk
import pygubu
from fandom_feudui import ClientUI


class Client(ClientUI):
    def __init__(self, master=None):
        super().__init__(master)


if __name__ == "__main__":
    app = Client()
    app.run()
