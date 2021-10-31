import logging
import tkinter as tk

from TkZero.Label import Label
from TkZero.Labelframe import Labelframe
from TkZero.Listbox import Listbox
from TkZero.Notebook import Tab, Notebook
from TkZero.Scrollbar import Scrollbar, OrientModes

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
        make_resizable(self.bundle_modules_frame, rows=0, cols=0)
        self.no_bundle_label = Label(self.bundle_modules_frame, text="No bundle is selected!")
        self.no_bundle_label.enabled = False
        self.no_bundle_label.grid(row=0, column=0, padx=1, pady=1, sticky=tk.NW)
        self.no_bundle_label.grid_remove()
        self.bundle_modules_listbox = Listbox(self.bundle_modules_frame, width=20, height=10)
        self.bundle_modules_listbox.grid(row=0, column=0, padx=1, pady=1, sticky=tk.NSEW)
        self.bundle_modules_vscroll = Scrollbar(self.bundle_modules_frame, widget=self.bundle_modules_listbox)
        self.bundle_modules_vscroll.grid(row=0, column=1, padx=1, pady=1)
        self.bundle_modules_hscroll = Scrollbar(self.bundle_modules_frame,
                                                orientation=OrientModes.Horizontal,
                                                widget=self.bundle_modules_listbox)
        self.bundle_modules_hscroll.grid(row=1, column=0, padx=1, pady=1)
        self.no_bundle_label.grid()
        self.bundle_modules_listbox.grid_remove()
        self.bundle_modules_vscroll.grid_remove()
        self.bundle_modules_hscroll.grid_remove()

    def update_bundle_modules(self):
        """
        Update the bundle modules.
        """
        logger.debug("Updating bundle modules")
        if self.cpybm.selected_bundle is not None:
            self.bundle_modules_frame.text = f"Modules in {self.cpybm.selected_bundle.title}"
            self.no_bundle_label.grid_remove()
            self.bundle_modules_listbox.grid()
            self.bundle_modules_vscroll.grid()
            self.bundle_modules_hscroll.grid()
        else:
            self.bundle_modules_frame.text = "Modules in selected bundle"
            self.no_bundle_label.grid()
            self.bundle_modules_listbox.grid_remove()
            self.bundle_modules_vscroll.grid_remove()
            self.bundle_modules_hscroll.grid_remove()

    def make_device_modules_frame(self):
        """
        Make the device modules frame.
        """
        self.device_modules_frame = Labelframe(self, text="Modules installed in selected device")
        self.device_modules_frame.grid(row=0, column=1, padx=1, pady=1, sticky=tk.NSEW)
        make_resizable(self.device_modules_frame, rows=0, cols=0)
        self.no_device_label = Label(self.device_modules_frame, text="No device is selected!")
        self.no_device_label.enabled = False
        self.no_device_label.grid(row=0, column=0, padx=1, pady=1, sticky=tk.NW)
        self.no_device_label.grid_remove()
        self.not_cpy_device_label = Label(self.device_modules_frame, text="Not a Circuitpython device!")
        self.not_cpy_device_label.enabled = False
        self.not_cpy_device_label.grid(row=0, column=0, padx=1, pady=1, sticky=tk.NW)
        self.not_cpy_device_label.grid_remove()
        self.device_modules_listbox = Listbox(self.device_modules_frame, width=20, height=10)
        self.device_modules_listbox.grid(row=0, column=0, padx=1, pady=1, sticky=tk.NSEW)
        self.device_modules_vscroll = Scrollbar(self.device_modules_frame, widget=self.device_modules_listbox)
        self.device_modules_vscroll.grid(row=0, column=1, padx=1, pady=1)
        self.device_modules_hscroll = Scrollbar(self.device_modules_frame,
                                                orientation=OrientModes.Horizontal,
                                                widget=self.device_modules_listbox)
        self.device_modules_hscroll.grid(row=1, column=0, padx=1, pady=1)
        self.no_device_label.grid()
        self.not_cpy_device_label.grid_remove()
        self.device_modules_listbox.grid_remove()
        self.device_modules_vscroll.grid_remove()
        self.device_modules_hscroll.grid_remove()

    def update_device_modules(self):
        """
        Update the device modules.
        """
        logger.debug("Updating device modules")
        if self.cpybm.selected_drive is not None \
                and self.cpybm.selected_drive.is_circuitpython:
            self.device_modules_frame.text = f"Modules installed in {self.cpybm.selected_drive.path}"
            self.no_device_label.grid_remove()
            self.not_cpy_device_label.grid_remove()
            self.device_modules_listbox.grid()
            self.device_modules_vscroll.grid()
            self.device_modules_hscroll.grid()
        else:
            if self.cpybm.selected_drive is None:
                self.no_device_label.grid()
                self.not_cpy_device_label.grid_remove()
                self.device_modules_frame.text = "Modules installed in selected device"
            else:
                self.no_device_label.grid_remove()
                self.not_cpy_device_label.grid()
                self.device_modules_frame.text = f"Modules installed in {self.cpybm.selected_drive.path}"
            self.device_modules_listbox.grid_remove()
            self.device_modules_vscroll.grid_remove()
            self.device_modules_hscroll.grid_remove()

    def make_do_stuff_buttons(self):
        """
        Make the buttons that do stuff. (like install, uninstall)
        """
