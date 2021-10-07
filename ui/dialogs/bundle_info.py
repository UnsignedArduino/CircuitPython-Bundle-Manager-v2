import logging
import tkinter as tk
import webbrowser

from TkZero.Dialog import CustomDialog
from TkZero.Entry import Entry
from TkZero.Label import Label

from helpers.create_logger import create_logger
from helpers.resize import make_resizable
from managers.bundle_manager import Bundle
from ui.widgets.clickable_label import ClickableLabel

logger = create_logger(name=__name__, level=logging.DEBUG)


def show_bundle_info(parent, bundle: Bundle):
    """
    Show info about a bundle in a dialog.

    :param parent: The parent of this window.
    :param bundle: The bundle to show information about.
    """
    dialog = CustomDialog(parent)
    name = bundle.title
    logger.debug(f"Showing information about bundle {bundle} ({name})")
    dialog.title = f"Info about bundle {name}"

    title_label = Label(dialog, text="Title: ")
    title_label.grid(row=0, column=0, padx=1, pady=1, sticky=tk.NW)
    title_entry = Entry(dialog, width=50)
    title_entry.value = bundle.title
    title_entry.read_only = True
    title_entry.grid(row=0, column=1, padx=1, pady=1, sticky=tk.NW + tk.E)

    tag_label = Label(dialog, text="Tag: ")
    tag_label.grid(row=1, column=0, padx=1, pady=1, sticky=tk.NW)
    tag_entry = Entry(dialog, width=50)
    tag_entry.value = bundle.tag_name
    tag_entry.read_only = True
    tag_entry.grid(row=1, column=1, padx=1, pady=1, sticky=tk.NW + tk.E)

    url_label = Label(dialog, text="URL to release: ")
    url_label.grid(row=3, column=0, padx=1, pady=1, sticky=tk.NW)
    url_click = ClickableLabel(dialog,
                               command=lambda: webbrowser.open(bundle.url))
    url_click.text = bundle.url
    url_click.grid(row=3, column=1, padx=1, pady=1, sticky=tk.NW + tk.E)

    released_label = Label(dialog, text="Released: ")
    released_label.grid(row=4, column=0, padx=1, pady=1, sticky=tk.NW)
    released_entry = Entry(dialog, width=50)
    DATE_FORMAT = "HH:mm:ss ddd, MMM Do, YYYY"
    released_entry.value = f"{bundle.released.format(DATE_FORMAT)} " \
                           f"({bundle.released.humanize()})"
    released_entry.read_only = True
    released_entry.grid(row=4, column=1, padx=1, pady=1, sticky=tk.NW + tk.E)

    versions_label = Label(dialog, text="Versions: ")
    versions_label.grid(row=5, column=0, padx=1, pady=1, sticky=tk.NW)
    versions_entry = Entry(dialog, width=50)
    versions_entry.value = ", ".join(bundle.versions)
    versions_entry.read_only = True
    versions_entry.grid(row=5, column=1, padx=1, pady=1, sticky=tk.NW + tk.E)

    make_resizable(dialog, range(0, 6), 1)
    dialog.resizable(True, False)

    dialog.bind("<Escape>", lambda _: dialog.close())

    dialog.grab_focus()
    dialog.wait_till_destroyed()
