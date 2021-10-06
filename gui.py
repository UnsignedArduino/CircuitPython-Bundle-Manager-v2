import logging
import tkinter as tk
from pathlib import Path

from PIL.ImageTk import PhotoImage
from TkZero.MainWindow import MainWindow
from TkZero.Notebook import Notebook, Tab

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
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.bundle_tab = Tab(self.notebook, "Bundle")
        self.modules_tab = Tab(self.notebook, "Modules")
        self.drive_tab = Tab(self.notebook, "Drive")
        self.other_tab = Tab(self.notebook, "Other")
        self.notebook.tabs += [self.bundle_tab, self.modules_tab,
                               self.drive_tab, self.other_tab]
        self.notebook.update_tabs()

    def load_icon(self):
        """
        Load the icon for the window.
        """
        logger.debug(f"Loading icon from {ICON_PATH}")
        icon = PhotoImage(file=ICON_PATH)
        self.icon = icon
