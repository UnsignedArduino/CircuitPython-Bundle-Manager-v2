import logging
import tkinter as tk
from pathlib import Path

from PIL.ImageTk import PhotoImage
from TkZero.MainWindow import MainWindow
from TkZero.Notebook import Notebook, Tab
from typing import Iterable, Union
import tkinter as tk

from circuitpython_bundle_manager import CircuitPythonBundleManager
from helpers.create_logger import create_logger

logger = create_logger(name=__name__, level=logging.DEBUG)

ICON_PATH = Path.cwd() / "icon.png"


class CircuitPythonBundleManagerGUI(MainWindow):
    """
    The GUI for the CircuitPython Bundle Manager v2.
    """
    def __init__(self):
        super().__init__()
        logger.debug("Initialize CircuitPythonBundleManager")
        self.cpybm = CircuitPythonBundleManager()
        logger.debug("Creating GUI")
        self.create_gui()
        self.title = "CircuitPython Bundle Manager v2"
        self.load_icon()

    def create_gui(self):
        """
        Create the widgets.
        """
        logger.debug("Creating widgets")
        self.create_notebook()

    def create_notebook(self):
        """
        Create the main notebook.
        """
        logger.debug("Creating notebook")
        self.notebook = Notebook(self)
        self.notebook.grid(row=0, column=0, padx=1, pady=1, sticky=tk.NSEW)
        self.make_resizable(self, 0, 0)
        self.bundle_tab = Tab(self.notebook, "Bundle")
        self.modules_tab = Tab(self.notebook, "Modules")
        self.drive_tab = Tab(self.notebook, "Drive")
        self.other_tab = Tab(self.notebook, "Other")
        self.notebook.tabs += [self.bundle_tab, self.modules_tab,
                               self.drive_tab, self.other_tab]
        self.notebook.update_tabs()

    def make_resizable(self, parent, rows: Union[Iterable, int],
                       cols: Union[Iterable, int], weight: int = 1):
        """
        Configure the rows and columns to have a weight of 1.

        :param parent: A Tkinter widget to use.
        :param rows: An Iterable or an int, specifying which row(s) to
         configure.
        :param cols: An Iterable or an int, specifying which column(s) to
         configure.
        :param weight: The weight to set. Defaults to 1.
        """
        if isinstance(rows, int):
            parent.rowconfigure(rows, weight=weight)
        else:
            for row in rows:
                parent.rowconfigure(row, weight=weight)
        if isinstance(cols, int):
            parent.columnconfigure(cols, weight=weight)
        else:
            for col in cols:
                parent.columnconfigure(col, weight=weight)

    def load_icon(self):
        """
        Load the icon for the window.
        """
        logger.debug(f"Loading icon from {ICON_PATH}")
        icon = PhotoImage(file=ICON_PATH)
        self.icon = icon
