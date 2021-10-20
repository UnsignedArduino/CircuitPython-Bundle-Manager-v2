import logging
import tkinter as tk

from TkZero.Button import Button
from TkZero.Combobox import Combobox
from TkZero.Frame import Frame
from TkZero.Label import Label
from TkZero.Notebook import Tab, Notebook

from circuitpython_bundle_manager import CircuitPythonBundleManager
from helpers.create_logger import create_logger
from helpers.resize import make_resizable

logger = create_logger(name=__name__, level=logging.DEBUG)


class DriveTab(Tab):
    """
    The DriveTab.
    """
    def __init__(self, parent: Notebook, cpybm: CircuitPythonBundleManager):
        """
        Make a DriveTab.

        :param parent: The parent of the tab. Should be a
         TkZero.Notebook.Notebook.
        :param cpybm: The CircuitPythonBundleManager instance.
        """
        super().__init__(parent, "Drive")
        self.cpybm = cpybm
        logger.debug("Making drive tab")
        self.make_gui()

    def make_gui(self):
        """
        Make the GUI for the drive tab.
        """
        logger.debug("Making GUI for drive tab")
        self.make_select_frame()
        make_resizable(self, cols=0)

    def make_select_frame(self):
        """
        Make the selected device frame.
        """
        self.select_frame = Frame(self)
        self.select_frame.grid(row=0, column=0, sticky=tk.NW + tk.E)
        make_resizable(self.select_frame, 0, 1)
        self.select_label = Label(self.select_frame, text="Selected device: ")
        self.select_label.grid(row=0, column=0, padx=1, pady=1, sticky=tk.NW)
        self.select_box = Combobox(self.select_frame, width=20)
        self.update_drives()
        self.select_box.grid(row=0, column=1, padx=1, pady=1, sticky=tk.NW + tk.E)
        self.select_refresh = Button(self.select_frame, text="Refresh",
                                     command=self.update_drives)
        self.select_refresh.grid(row=0, column=2, padx=1, pady=0, sticky=tk.NE)

    def update_drives(self):
        """
        Update all connected drives.
        """
        logger.debug("Updating connected drives")
        self.select_frame.enabled = False
        self.update()
        self.select_box.read_only = False
        self.drive_dict = {"None": None}
        self.cpybm.device_manager.index_drives()
        for drive in self.cpybm.device_manager.circuitpython_drives:
            self.drive_dict[str(drive.path) + " (CircuitPython drive)"] = drive
        for drive in self.cpybm.device_manager.drives:
            self.drive_dict[str(drive.path)] = drive
        self.select_box.values = self.drive_dict.keys()
        self.select_box.value = self.select_box.values[0]
        self.select_box.read_only = True
        self.select_frame.enabled = True
