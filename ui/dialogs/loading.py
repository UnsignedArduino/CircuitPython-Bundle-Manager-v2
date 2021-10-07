import logging
import tkinter as tk

from TkZero.Dialog import CustomDialog
from TkZero.Label import Label
from TkZero.Progressbar import Progressbar, ProgressModes

from helpers.create_logger import create_logger
from helpers.resize import make_resizable

logger = create_logger(name=__name__, level=logging.DEBUG)


def show_deleting(parent, name: str) -> CustomDialog:
    """
    Show info about a bundle in a dialog.

    :param parent: The parent of this window.
    :param name: The name of the deleted bundle
    """
    dialog = CustomDialog(parent)
    dialog.title = f"Removing bundle {name}"

    title_label = Label(dialog, text=f"Removing bundle {name}...")
    title_label.grid(row=0, column=0, padx=1, pady=1, sticky=tk.NW)

    pb = Progressbar(dialog, length=200, mode=ProgressModes.Indeterminate,
                     allow_text=False)
    pb.start()
    pb.grid(row=1, column=0, padx=1, pady=1, sticky=tk.NW + tk.E)

    make_resizable(dialog, range(0, 2), 0)

    dialog.resizable(False, False)

    dialog.grab_focus()
    return dialog
