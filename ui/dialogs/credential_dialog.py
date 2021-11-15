"""
CircuitPython Bundle Manager v2 - a Python program to easily manage
modules on a CircuitPython device!

Copyright (C) 2021 UnsignedArduino

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import logging
import tkinter as tk

from TkZero.Button import Button
from TkZero.Dialog import show_info, show_error
from TkZero.Checkbutton import Checkbutton
from TkZero.Dialog import CustomDialog
from TkZero.Entry import Entry
from TkZero.Frame import Frame
from TkZero.Label import Label

from helpers.create_logger import create_logger
from helpers.resize import make_resizable
from managers.credential_manager import CredentialManager

logger = create_logger(name=__name__, level=logging.DEBUG)


def show_credential_manager(parent, cred: CredentialManager):
    """
    Show the credential manager dialog.

    :param parent: The parent of this window.
    :param cred: The credential manager instance.
    """
    dialog = CustomDialog(parent)
    logger.debug(f"Showing credential manager dialog")
    dialog.title = "CircuitPython Bundle Manager v2: Credential Manager"
    make_resizable(dialog, range(0, 2), 0)

    token_frame = Frame(dialog)
    token_frame.grid(row=0, column=0, sticky=tk.NSEW)
    make_resizable(token_frame, 0, 1)

    token_label = Label(token_frame, text="GitHub Token:")
    token_label.grid(row=0, column=0, padx=1, pady=1, sticky=tk.NW)

    token_entry = Entry(token_frame, width=50, show="*")
    if cred.has_github_token(in_keyring=True):
        token_entry.value = cred.get_github_token()
    token_entry.grid(row=0, column=1, padx=1, pady=1, sticky=tk.NW + tk.E)

    def toggle_show():
        if token_show.value:
            token_entry.configure(show="")
        else:
            token_entry.configure(show="*")

    token_show = Checkbutton(token_frame, text="Show?",
                             command=toggle_show)
    token_show.grid(row=0, column=2, padx=1, pady=1, sticky=tk.NE)

    buttons_frame = Frame(dialog)
    buttons_frame.grid(row=1, column=0, sticky=tk.NSEW)
    make_resizable(buttons_frame, range(0, 4), 0)

    def load():
        try:
            token_entry.value = cred.get_github_token()
        except Exception as e:
            show_error(dialog, title="CircuitPython Bundle Manager v2: Error!",
                       message="There was an error loading the saved GitHub token!",
                       detail=str(e))
        else:
            show_info(dialog, title="CircuitPython Bundle Manager v2: Info",
                      message="Successfully loaded GitHub token!")
        update_buttons()

    load_button = Button(buttons_frame, text="Load saved token",
                         command=load)
    load_button.grid(row=0, column=0, padx=1, pady=1, sticky=tk.NW + tk.E)

    def save():
        try:
            cred.set_github_token(token_entry.value)
        except Exception as e:
            show_error(dialog, title="CircuitPython Bundle Manager v2: Error!",
                       message="There was an error saving the GitHub token!",
                       detail=str(e))
        else:
            show_info(dialog, title="CircuitPython Bundle Manager v2: Info",
                      message="Successfully saved GitHub token!")
        update_buttons()

    save_button = Button(buttons_frame, text="Save current token",
                         command=save)
    save_button.grid(row=0, column=1, padx=1, pady=1, sticky=tk.NW + tk.E)

    def delete():
        try:
            cred.delete_github_token()
        except Exception as e:
            show_error(dialog, title="CircuitPython Bundle Manager v2: Error!",
                       message="There was an error deleting the saved GitHub token!",
                       detail=str(e))
        else:
            show_info(dialog, title="CircuitPython Bundle Manager v2: Info",
                      message="Successfully deleted saved GitHub token!")
        update_buttons()

    delete_button = Button(buttons_frame, text="Delete saved token",
                           command=delete)
    delete_button.grid(row=0, column=2, padx=1, pady=1, sticky=tk.NW + tk.E)

    def update_buttons():
        if cred.has_github_token(in_keyring=True):
            load_button.enabled = True
            save_button.enabled = len(token_entry.value) > 0
            delete_button.enabled = True
        else:
            load_button.enabled = False
            save_button.enabled = len(token_entry.value) > 0
            delete_button.enabled = False

    update_buttons()
    token_entry._variable.trace_add("write", lambda *args: update_buttons())

    close_button = Button(buttons_frame, text="Close",
                          command=dialog.close)
    close_button.grid(row=0, column=3, padx=1, pady=1, sticky=tk.NW + tk.E)

    dialog.resizable(True, False)
    dialog.bind("<Escape>", lambda _: dialog.close())

    dialog.grab_focus()
    dialog.wait_till_destroyed()
