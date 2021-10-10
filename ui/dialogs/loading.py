import logging
import tkinter as tk

from TkZero.Dialog import CustomDialog
from TkZero.Label import Label
from TkZero.Progressbar import Progressbar, ProgressModes

from helpers.create_logger import create_logger
from helpers.resize import make_resizable

logger = create_logger(name=__name__, level=logging.DEBUG)


def show_indeterminate(parent, title: str, label: str) -> CustomDialog:
    """
    Show a generic loading dialog.

    :param parent: The parent of this window.
    :param title: The title of the dialog.
    :param label: THe label of the dialog.
    """
    dialog = CustomDialog(parent)
    dialog.title = title

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


def show_determinate(parent, title: str, label: str) -> tuple[CustomDialog,
                                                              Progressbar]:
    """
    Show a generic loading dialog.

    :param parent: The parent of this window.
    :param title: The title of the dialog.
    :param label: THe label of the dialog.
    """
    dialog = CustomDialog(parent)
    dialog.title = title

    title_label = Label(dialog, text=label)
    title_label.grid(row=0, column=0, padx=1, pady=1, sticky=tk.NW)

    pb = Progressbar(dialog, length=300, allow_text=False)
    pb.grid(row=1, column=0, padx=1, pady=1, sticky=tk.NW + tk.E)

    make_resizable(dialog, range(0, 2), 0)

    dialog.resizable(False, False)

    dialog.grab_focus()
    return dialog, pb


def show_determinate_with_label(parent, title: str, label: str) -> \
        tuple[CustomDialog, Progressbar, Label]:
    """
    Show a generic loading dialog.

    :param parent: The parent of this window.
    :param title: The title of the dialog.
    :param label: THe label of the dialog.
    """
    dialog = CustomDialog(parent)
    dialog.title = title

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
    Show info about a bundle in a dialog.

    :param parent: The parent of this window.
    :param name: The name of the deleted bundle
    """
    return show_indeterminate(parent, f"Removing bundle {name}",
                              f"Removing bundle {name}...")


def show_get_releases(parent) -> tuple[CustomDialog, Progressbar]:
    """
    Show loading dialog saying that we are getting the releases.

    :param parent: The parent of this window.
    """
    return show_determinate(parent, f"Getting all releases",
                            f"Getting releases available to download...")


def show_download_release(parent) -> tuple[CustomDialog, Progressbar, Label]:
    """
    Show loading dialog saying that we are downloading the release.

    :param parent: The parent of this window.
    """
    return show_determinate_with_label(parent, f"Downloading release",
                                       f"Downloading release...")
