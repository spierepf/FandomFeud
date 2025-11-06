#!/usr/bin/python3
import json
import pathlib
import tkinter as tk
from logging import exception
from tkinter import ttk, filedialog, messagebox

import pygubu
from clientui import ClientUI
import logging

from os.path import dirname, abspath, join
import sys
sys.path.append(abspath(join(dirname(__file__), '..')))
from core.rpc import RPCClient
from core.side import Side

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
import styles  # Styles definition module


class Client(ClientUI):
    def __init__(self, master=None, on_first_object_cb=None):
        super().__init__(master, on_first_object_cb=styles.setup_ttk_styles)
        self.model = None
        self.event_var = self.builder.get_variable("event_var")
        self.disable_all(self.builder.get_object("round_frame"))

    def _navigate_widget_tree(self, widget, cond=None, op=None):
        if callable(getattr(widget, 'winfo_children', None)):
            for child in widget.winfo_children():
                self._navigate_widget_tree(child, cond, op)
        if cond is None or cond(widget):
            if op is not None:
                op(widget)

    def disable_all(self, widget):
        self._navigate_widget_tree(widget,
                                   lambda w: type(w) in [ttk.Button, ttk.Radiobutton, ttk.Entry],
                                   lambda w: w.config(state=tk.DISABLED))

    def enable_all(self, widget):
        self._navigate_widget_tree(widget,
                                   lambda w: type(w) in [ttk.Button, ttk.Radiobutton, ttk.Entry],
                                   lambda w: w.config(state=tk.NORMAL))

    def connect_to_server(self):
        host = self.builder.get_variable("host_var").get()
        port = self.builder.get_variable("port_var").get()
        logger.info(f"Connecting to {host} on port {port}")
        try:
            self.model = RPCClient(host, port)
            self.model.connect()
            self.enable_all(self.builder.get_object("round_frame"))
        except Exception as e:
            logger.exception(f"While connecting to {host} on port {port}")
            messagebox.showerror('Connection Error', str(e))
        self.disable_all(self.builder.get_object("connect_frame"))

    def set_timer_duration(self):
        self.model.set_timer_duration(self.builder.get_variable('duration_entry_var').get())

    def start_timer(self):
        self.model.set_timer_start(True)

    def play_duplicate_sound(self):
        self.model.set_play_duplicate_sound(True)

    def commit(self):
        event = self.event_var.get()
        logger.info(f"Committing {event}")
        next_event = 'reveal_score_0'

        match event:
            case event if event.startswith('reveal_answer_'):
                i = int(event[-1])
                answer = self.builder.get_variable(f'answer_{i}_entry_var').get()
                if answer is not None:
                    self.model.set_answer(i, answer)
                    self.model.set_play_reveal_sound(True)
                    next_event = f'reveal_score_{i}'


            case event if event.startswith('reveal_score_'):
                i = int(event[-1])
                next_event = f'reveal_answer_{(i+1)%10}'
                score = self.builder.get_variable(f'score_{i}_entry_var').get()
                if score is not None:
                    self.model.set_score(i, score)
                    if score > 0:
                        self.model.set_play_points_sound(True)
                    else:
                        self.model.set_play_no_points_sound(True)

        self.builder.get_variable('event_var').set(next_event)




if __name__ == "__main__":
    app = Client()
    app.run()
