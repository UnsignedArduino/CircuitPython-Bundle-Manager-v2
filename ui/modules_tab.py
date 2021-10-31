import logging
import tkinter as tk

from TkZero.Labelframe import Labelframe
from TkZero.Notebook import Tab, Notebook

from circuitpython_bundle_manager import CircuitPythonBundleManager
from helpers.create_logger import create_logger
from helpers.resize import make_resizable

logger = create_logger(name=__name__, level=logging.DEBUG)


class ModulesTab(Tab):
    """
    The ModulesTab.
    """
    def __init__(self, parent: Notebook, cpybm: CircuitPythonBundleManager):
        """
        Make a ModulesTab.

        :param parent: The parent of the tab. Should be a
         TkZero.Notebook.Notebook.
        :param cpybm: The CircuitPythonBundleManager instance.
        """
        super().__init__(parent, "Modules")
        self.cpybm = cpybm
        logger.debug("Making modules tab")
        self.make_gui()

    def make_gui(self):
        """
        Make the GUI for this tab.
        """
        self.make_bundle_modules_frame()
        self.make_device_modules_frame()
        self.make_do_stuff_buttons()
        make_resizable(self, rows=0, cols=range(0, 2))
        make_resizable(self, rows=1, cols=0)
        self.register_callbacks()

    def register_callbacks(self):
        """
        Register callbacks when the selected device or module changes.
        """
        self.cpybm.on_new_selected_bundle = self.update_bundle_modules
        self.cpybm.on_new_selected_drive = self.update_device_modules

    def make_bundle_modules_frame(self):
        """
        Make the bundle modules frame.
        """
        self.bundle_modules_frame = Labelframe(self, text="Modules in selected bundle")
        self.bundle_modules_frame.grid(row=0, column=0, padx=1, pady=1, sticky=tk.NSEW)

    def update_bundle_modules(self):
        """
        Update the bundle modules.
        """
        logger.debug("Updating bundle modules")
        if self.cpybm.selected_bundle is not None:
            self.bundle_modules_frame.text = f"Modules in {self.cpybm.selected_bundle.title}"
        else:
            self.bundle_modules_frame.text = "Modules in selected bundle"

    def make_device_modules_frame(self):
        """
        Make the device modules frame.
        """
        self.device_modules_frame = Labelframe(self, text="Modules installed in selected device")
        self.device_modules_frame.grid(row=0, column=1, padx=1, pady=1, sticky=tk.NSEW)

    def update_device_modules(self):
        """
        Update the device modules.
        """
        logger.debug("Updating device modules")
        if self.cpybm.selected_drive is not None:
            self.device_modules_frame.text = f"Modules installed in {self.cpybm.selected_drive.path}"
        else:
            self.device_modules_frame.text = "Modules installed in selected device"

    def make_do_stuff_buttons(self):
        """
        Make the buttons that do stuff. (like install, uninstall)
        """
