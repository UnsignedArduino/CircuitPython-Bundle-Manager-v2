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

from PIL.ImageTk import PhotoImage
from TkZero.MainWindow import MainWindow
from TkZero.Notebook import Notebook

from circuitpython_bundle_manager import CircuitPythonBundleManager
from helpers.create_logger import create_logger
from helpers.resize import make_resizable
from ui.bundle_tab import BundleTab
from ui.drive_tab import DriveTab
from ui.modules_tab import ModulesTab
from ui.other_tab import OtherTab

logger = create_logger(name=__name__, level=logging.DEBUG)

ICON_PATH = Path.cwd() / "icon.png"


class CircuitPythonBundleManagerGUI(MainWindow):
    """
    The GUI for the CircuitPython Bundle Manager v2.
    """
    def __init__(self, settings_path: Path):
        super().__init__()
        self.settings_path = settings_path
        logger.debug("Initialize CircuitPythonBundleManager")
        self.cpybm = CircuitPythonBundleManager(settings_path)
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
        make_resizable(self, 0, 0)
        self.notebook.tabs += [BundleTab(self.notebook, self.cpybm),
                               ModulesTab(self.notebook, self.cpybm),
                               DriveTab(self.notebook, self.cpybm),
                               OtherTab(self.notebook, self.cpybm, self.settings_path)]
        self.notebook.update_tabs()

    def load_icon(self):
        """
        Load the icon for the window.
        """
        logger.debug(f"Loading icon from {ICON_PATH}")
        icon = PhotoImage(file=ICON_PATH)
        # self.icon = icon
        self.tk.call("wm", "iconphoto", self, "-default", icon)
