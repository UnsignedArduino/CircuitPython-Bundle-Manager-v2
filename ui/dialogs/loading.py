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

from TkZero.Dialog import CustomDialog
from TkZero.Label import Label
from TkZero.Progressbar import Progressbar, ProgressModes

from helpers.create_logger import create_logger
from helpers.resize import make_resizable
from typing import Callable

logger = create_logger(name=__name__, level=logging.DEBUG)


def show_indeterminate(parent, title: str, label: str,
                       on_close: Callable = lambda: None) -> CustomDialog:
    """
    Show a generic loading dialog.

    :param parent: The parent of this window.
    :param title: The title of the dialog.
    :param label: THe label of the dialog.
    :param on_close: The function to run when this dialog is closed.
    """
    dialog = CustomDialog(parent)
    dialog.title = title
    dialog.on_close = on_close

    title_label = Label(dialog, text=label)
    title_label.grid(row=0, column=0, padx=1, pady=1, sticky=tk.NW)

    pb = Progressbar(dialog, length=300, mode=ProgressModes.Indeterminate,
                     allow_text=False)
    pb.start()
    pb.grid(row=1, column=0, padx=1, pady=1, sticky=tk.NW + tk.E)

    make_resizable(dialog, range(0, 2), 0)

    dialog.resizable(False, False)

    dialog.grab_focus()
    return dialog


def show_determinate(parent, title: str, label: str,
                     on_close: Callable = lambda: None) -> tuple[CustomDialog,
                                                                 Progressbar]:
    """
    Show a generic loading dialog.

    :param parent: The parent of this window.
    :param title: The title of the dialog.
    :param label: THe label of the dialog.
    :param on_close:The function to run when this dialog is closed.
    """
    dialog = CustomDialog(parent)
    dialog.title = title
    dialog.on_close = on_close

    title_label = Label(dialog, text=label)
    title_label.grid(row=0, column=0, padx=1, pady=1, sticky=tk.NW)

    pb = Progressbar(dialog, length=300, allow_text=False)
    pb.grid(row=1, column=0, padx=1, pady=1, sticky=tk.NW + tk.E)

    make_resizable(dialog, range(0, 2), 0)

    dialog.resizable(False, False)

    dialog.grab_focus()
    return dialog, pb


def show_determinate_with_label(parent, title: str, label: str,
                                on_close: Callable = lambda: None) -> \
        tuple[CustomDialog, Progressbar, Label]:
    """
    Show a generic loading dialog.

    :param parent: The parent of this window.
    :param title: The title of the dialog.
    :param label: THe label of the dialog.
    :param on_close:The function to run when this dialog is closed.
    """
    dialog = CustomDialog(parent)
    dialog.title = title
    dialog.on_close = on_close

    title_label = Label(dialog, text=label)
    title_label.grid(row=0, column=0, padx=1, pady=1, sticky=tk.NW)

    pb = Progressbar(dialog, length=300, allow_text=False)
    pb.grid(row=1, column=0, padx=1, pady=1, sticky=tk.NW + tk.E)

    progress_label = Label(dialog)
    progress_label.grid(row=2, column=0, padx=1, pady=1, sticky=tk.NW)

    make_resizable(dialog, range(0, 3), 0)

    dialog.resizable(False, False)

    dialog.grab_focus()
    return dialog, pb, progress_label


def show_deleting(parent, name: str) -> CustomDialog:
    """
    Show loading dialog saying that we are deleting a bundle.

    :param parent: The parent of this window.
    :param name: The name of the deleted bundle.
    """
    return show_indeterminate(parent, f"Removing bundle {name}",
                              f"Removing bundle {name}...")


def show_installing(parent, name: str) -> CustomDialog:
    """
    Show loading dialog saying that we are installing a module.

    :param parent: The parent of this window.
    :param name: The name of the installing module.
    """
    return show_indeterminate(parent, f"Installing module {name}",
                              f"Installing module {name}...")


def show_uninstalling(parent, name: str) -> CustomDialog:
    """
    Show loading dialog saying that we are uninstalling a module.

    :param parent: The parent of this window.
    :param name: The name of the uninstalling module.
    """
    return show_indeterminate(parent, f"Uninstalling module {name}",
                              f"Uninstalling module {name}...")


def show_reinstalling(parent, name: str) -> CustomDialog:
    """
    Show loading dialog saying that we are reinstalling a module.

    :param parent: The parent of this window.
    :param name: The name of the reinstalling module.
    """
    return show_indeterminate(parent, f"Reinstalling module {name}",
                              f"Reinstalling module {name}...")


def show_get_releases(parent, on_close: Callable) -> tuple[CustomDialog, Progressbar]:
    """
    Show loading dialog saying that we are getting the releases.

    :param parent: The parent of this window.
    :param on_close: The function to call when this window is closed.
    """
    return show_determinate(parent, f"Getting all releases",
                            f"Getting releases available to download...",
                            on_close)


def show_download_release(parent) -> tuple[CustomDialog, Progressbar, Label]:
    """
    Show loading dialog saying that we are downloading the release.

    :param parent: The parent of this window.
    """
    return show_determinate_with_label(parent, f"Downloading release",
                                       f"Downloading release...")
