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
from pathlib import Path

from TkZero.Dialog import CustomDialog
from TkZero.Text import Text, TextWrap
from TkZero.Scrollbar import Scrollbar, OrientModes

from helpers.resize import make_resizable
from helpers.create_logger import create_logger

logger = create_logger(name=__name__, level=logging.DEBUG)


def show_text_file(parent, title: str, filepath: Path):
    """
    Show a dialog with a text box to display some text.

    :param parent: The parent of the window.
    :param title: The title of the window.
    :param filepath: A path to a text file.
    """
    logger.debug(f"Showing text from file {filepath}")
    show_text(parent, title, filepath.read_text())


def show_text(parent, title: str, text: str):
    """
    Show a dialog with a text box to display some text.

    :param parent: The parent of the window.
    :param title: The title of the window.
    :param text: The text to display.
    """
    logger.debug(f"Showing text of length {len(text)}")
    dlg = CustomDialog(parent)
    dlg.title = title
    make_resizable(dlg, rows=0, cols=0)
    txt = Text(dlg, width=72, height=20, wrapping=TextWrap.NoWrapping)
    txt.text = text
    txt.read_only = True
    txt.grid(row=0, column=0, padx=1, pady=1, sticky=tk.NSEW)
    y = Scrollbar(dlg, widget=txt)
    y.grid(row=0, column=1, padx=1, pady=1)
    x = Scrollbar(dlg, orientation=OrientModes.Horizontal, widget=txt)
    x.grid(row=1, column=0, padx=1, pady=1)
    dlg.grab_focus()
    dlg.wait_till_destroyed()
