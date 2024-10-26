#!/usr/bin/python3
import json
import pathlib
import tkinter as tk
from logging import exception
from tkinter import ttk, filedialog, messagebox

import pygubu
from fandom_feudui import ClientUI
import logging

from rpc import RPCClient
from side import Side

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class Client(ClientUI):
    def __init__(self, master=None):
        super().__init__(master)
        self.model = None
        self.event_var = self.builder.get_variable("event_var")

        self.pot_score_var = self.builder.get_variable("pot_score_var")
        self.pot_score_var.trace_add("write", self.update_pot_score_var)

        self.left_score_var = self.builder.get_variable("left_score_var")
        self.left_score_var.trace_add("write", self.update_left_score_var)

        self.right_score_var = self.builder.get_variable("right_score_var")
        self.right_score_var.trace_add("write", self.update_right_score_var)

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

    def get_pot_score(self):
        try:
            return self.pot_score_var.get()
        except tk.TclError:
            return None

    def get_left_score(self):
        try:
            return self.left_score_var.get()
        except tk.TclError:
            return None

    def get_right_score(self):
        try:
            return self.right_score_var.get()
        except tk.TclError:
            return None

    def ensure_connected(self):
        connected = self.model is not None and self.model.is_connected()
        if not connected:
            messagebox.showwarning("Not Connected", "We are no longer connected to the server")
        return connected

    def update_pot_score_var(self, name, index, operation):
        pot_score = self.get_pot_score()
        if pot_score is not None and self.ensure_connected():
            self.model.set_pot(pot_score)

    def update_left_score_var(self, name, index, operation):
        left_score = self.get_left_score()
        if left_score is not None and self.ensure_connected():
            self.model.set_score(Side.LEFT.value, left_score)

    def update_right_score_var(self, name, index, operation):
        right_score = self.get_right_score()
        if right_score is not None and self.ensure_connected():
            self.model.set_score(Side.RIGHT.value, right_score)

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

    def begin_round(self):
        with filedialog.askopenfile(filetypes=[('JSON', '.json')], defaultextension='.json') as load_file:
            answers_frame = self.builder.get_object("answers_frame")
            for widget in answers_frame.winfo_children():
                widget.destroy()
            answers = json.loads(load_file.read())['answers']
            for i in range(len(answers)):
                answer_frame = ttk.Frame(answers_frame, name=f"answer_frame_{i}")
                ttk.Label(answer_frame, text=answers[i][0], width=20).pack(side=tk.LEFT)
                ttk.Label(answer_frame, text=answers[i][1], width=2).pack(side=tk.LEFT)

                reveal_and_score_radiobutton = ttk.Radiobutton(answer_frame, text="Reveal and Score", variable=self.builder.get_variable("event_var"), value=f"reveal_and_score_{i}")
                reveal_and_score_radiobutton.pack(side=tk.LEFT)

                reveal_only_radiobutton = ttk.Radiobutton(answer_frame, text="Reveal Only", variable=self.builder.get_variable("event_var"), value=f"reveal_only_{i}")
                reveal_only_radiobutton.pack(side=tk.LEFT)
                answer_frame.pack()
            self.model.begin_round(answers)

    def add_answer_score_to_pot(self, i):
        self.pot_score_var.set(self.pot_score_var.get() + self.model.get_answer_score(i) * self.builder.get_variable("round_multiplier_var").get())

    def reveal_answer(self, i):
        self.model.reveal_answer(i)
        self.disable_all(self.builder.get_object("answers_frame").winfo_children()[i])

    def set_strike(self, i):
        self.model.set_strike(i)

    def commit(self):
        event = self.event_var.get()
        logger.info(f"Committing {event}")

        match event:
            case 'award_pot_to_left':
                self.left_score_var.set(self.get_left_score() + self.get_pot_score())
                self.pot_score_var.set(0)
            case 'award_pot_to_right':
                self.right_score_var.set(self.get_right_score() + self.get_pot_score())
                self.pot_score_var.set(0)
            case event if event.startswith('reveal_and_score_'):
                i = int(event[-1])
                self.reveal_answer(i)
                self.add_answer_score_to_pot(i)
            case event if event.startswith('reveal_only_'):
                self.reveal_answer(int(event[-1]))
            case event if event.startswith('strike_'):
                self.set_strike(int(event[-1]))
            case 'failed_steal':
                self.set_strike(1)




if __name__ == "__main__":
    app = Client()
    app.run()
