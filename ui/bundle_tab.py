import logging
import tkinter as tk
from threading import Thread

from TkZero.Button import Button
from TkZero.Frame import Frame
from TkZero.Label import Label
from TkZero.Listbox import Listbox
from TkZero.Notebook import Tab, Notebook
from TkZero.Scrollbar import Scrollbar
from TkZero.Separator import Separator, OrientModes

from circuitpython_bundle_manager import CircuitPythonBundleManager
from helpers.create_logger import create_logger
from helpers.resize import make_resizable
from ui.dialogs.bundle_info import show_bundle_info

logger = create_logger(name=__name__, level=logging.DEBUG)


class BundleTab(Tab):
    """
    The BundleTab.
    """
    def __init__(self, parent: Notebook, cpybm: CircuitPythonBundleManager):
        """
        Make a BundleTab.

        :param parent: The parent of the tab. Should be a
         TkZero.Notebook.Notebook.
        :param cpybm: The CircuitPythonBundleManager instance.
        """
        super().__init__(parent, "Bundle")
        self.cpybm = cpybm
        logger.debug("Making bundle tab")
        self.make_gui()

    def make_gui(self):
        """
        Make the GUI.
        """
        logger.debug("Making GUI")
        self.make_bundle_listbox()
        self.make_buttons()
        self.selected_label = Label(self, text="")
        self.selected_label.grid(row=0, column=0, columnspan=2,
                                 padx=1, pady=1, sticky=tk.NW)
        self.update_buttons()
        self.update_selected_bundle()
        self.update_bundle_listbox()
        make_resizable(self, 1, 0)

    def make_buttons(self):
        """
        Make the buttons.
        """
        self.buttons_frame = Frame(self)
        self.buttons_frame.grid(row=1, column=1, sticky=tk.NSEW)
        self.add_button = Button(self.buttons_frame, text="Add bundle...")
        self.add_button.grid(row=0, column=0, padx=1, pady=1, sticky=tk.NSEW)
        self.pop_button = Button(self.buttons_frame, text="Remove bundle")
        self.pop_button.grid(row=1, column=0, padx=1, pady=1, sticky=tk.NSEW)
        Separator(self.buttons_frame, orientation=OrientModes.Horizontal).grid(
            row=2, column=0, padx=1, pady=1, sticky=tk.NSEW)
        self.select_button = Button(self.buttons_frame, text="Use bundle",
                                    command=self.update_selected_bundle)
        self.select_button.grid(row=3, column=0, padx=1, pady=1, sticky=tk.NSEW)
        Separator(self.buttons_frame, orientation=OrientModes.Horizontal).grid(
            row=4, column=0, padx=1, pady=1, sticky=tk.NSEW)
        self.info_button = Button(self.buttons_frame, text="Bundle info",
                                  command=self.show_bundle_info)
        self.info_button.grid(row=5, column=0, padx=1, pady=1, sticky=tk.NSEW)
        Separator(self.buttons_frame, orientation=OrientModes.Horizontal).grid(
            row=6, column=0, padx=1, pady=1, sticky=tk.NSEW)
        self.refresh_button = Button(self.buttons_frame, text="Refresh",
                                     command=self.update_bundle_listbox)
        self.refresh_button.grid(row=7, column=0, padx=1, pady=1, sticky=tk.NSEW)

    def show_bundle_info(self):
        """
        Show info about the bundle.
        """
        bundle = self.bundles[self.listbox.selected[0]]
        logger.debug(f"Showing info about {bundle}")
        show_bundle_info(self, bundle)

    def update_buttons(self):
        """
        Update the button states.
        """
        logger.debug("Updating button states")
        if len(self.listbox.selected) == 0:
            self.pop_button.enabled = False
            self.select_button.enabled = False
            self.info_button.enabled = False
        else:
            self.pop_button.enabled = True
            self.select_button.enabled = True
            self.info_button.enabled = True

    def update_selected_bundle(self):
        """
        Update the selected bundle.
        """
        if len(self.listbox.selected) == 0:
            logger.debug(f"Selected bundle: None")
            self.selected_label.text = "Selected bundle: None"
        else:
            name = self.listbox.values[self.listbox.selected[0]]
            bundle = self.bundles[self.listbox.selected[0]]
            self.cpybm.selected_bundle = bundle
            logger.debug(f"Selected bundle: {bundle}")
            self.selected_label.text = f"Selected bundle: {name}"

    def make_bundle_listbox(self):
        """
        Make the bundle listbox and scrollbar and stuff.
        """
        self.listbox_frame = Frame(self)
        self.listbox_frame.grid(row=1, column=0, sticky=tk.NSEW)
        self.listbox = Listbox(self.listbox_frame, width=50, height=10,
                               on_select=self.update_buttons)
        self.listbox.grid(row=0, column=0, padx=(1, 0), pady=1, sticky=tk.NSEW)
        self.listbox_scroll = Scrollbar(self.listbox_frame, widget=self.listbox)
        self.listbox_scroll.grid(row=0, column=1, padx=(0, 1), pady=1)
        make_resizable(self.listbox_frame, 0, 0)

    def update_bundle_listbox(self):
        """
        Update the list of bundles available.
        """
        logger.debug("Updating list of bundles")
        self.listbox_frame.enabled = False
        self.buttons_frame.enabled = False
        self.bundles = []

        def update():
            self.cpybm.bundle_manager.index_bundles()
            self.bundles = self.cpybm.bundle_manager.bundles
            self.listbox.values = [b.title for b in self.bundles]
            self.listbox_frame.enabled = True
            self.buttons_frame.enabled = True
            self.update_buttons()

        t = Thread(target=update, daemon=True)
        logger.debug(f"Spawning thread {t}")
        t.start()
