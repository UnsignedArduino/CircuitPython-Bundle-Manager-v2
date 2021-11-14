import logging
from typing import Callable
import tkinter as tk
from threading import Thread

from TkZero.Button import Button
from TkZero.Dialog import ask_ok_or_cancel, show_error, show_info
from TkZero.Frame import Frame
from TkZero.Label import Label
from TkZero.Listbox import Listbox
from TkZero.Notebook import Tab, Notebook
from TkZero.Scrollbar import Scrollbar
from TkZero.Separator import Separator, OrientModes

from circuitpython_bundle_manager import CircuitPythonBundleManager
from helpers.create_logger import create_logger
from helpers.resize import make_resizable
from ui.dialogs.add_bundle import add_bundle_dialog
from ui.dialogs.bundle_info import show_bundle_info
from ui.dialogs.loading import show_deleting

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
        Separator(self, orientation=OrientModes.Horizontal).grid(
            row=1, column=0, columnspan=2, padx=1, pady=1, sticky=tk.NSEW)
        self.downloaded_bundles_label = Label(self, text="Downloaded bundles: ")
        self.downloaded_bundles_label.grid(row=2, column=0, columnspan=2,
                                           padx=1, pady=1, sticky=tk.NW)
        self.update_buttons()
        self.update_selected_bundle()
        self.update_bundle_listbox(self.load_last_selected_bundle)
        make_resizable(self, 3, 0)

    def make_buttons(self):
        """
        Make the buttons.
        """
        self.buttons_frame = Frame(self)
        self.buttons_frame.grid(row=3, column=1, sticky=tk.NSEW)
        self.add_button = Button(self.buttons_frame, text="Add bundle...",
                                 command=self.add_bundle)
        self.add_button.grid(row=0, column=0, padx=1, pady=1, sticky=tk.NSEW)
        self.pop_button = Button(self.buttons_frame, text="Remove bundle",
                                 command=self.pop_bundle)
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

    def add_bundle(self):
        """
        Download a new bundle.
        """
        try:
            add_bundle_dialog(self, self.cpybm)
        except tk.TclError:
            pass
        except Exception as e:
            show_error(self, title="CircuitPython Bundle Manager v2: Error!",
                       message="Error while downloading new bundle!",
                       detail=str(e))
        finally:
            self.update_bundle_listbox()

    def pop_bundle(self):
        """
        Pop the currently selected bundle.
        """
        name = self.listbox.values[self.listbox.selected[0]]
        bundle = self.bundles[self.listbox.selected[0]]
        if not ask_ok_or_cancel(self, title="CircuitPython Bundle Manager v2: Confirm",
                                message="Are you sure you want to delete "
                                        "the selected bundle?",
                                detail=f"Selected bundle: {bundle.title}"):
            return
        dialog = show_deleting(self, bundle.title)
        logging.debug(f"Deleting bundle {bundle}")

        self.listbox_frame.enabled = False
        self.buttons_frame.enabled = False

        def delete():
            try:
                self.cpybm.delete_bundle(bundle)
            except Exception as e:
                logger.exception("Exception while deleting bundle")
                show_error(self, title="CircuitPython Bundle Manager v2: Error!",
                           message="Error while deleting bundle!",
                           detail=str(e))
            else:
                show_info(self, title="CircuitPython Bundle Manager v2: Info",
                          message="Successfully deleted bundle!")
            self.cpybm.selected_bundle = None
            self.listbox_frame.enabled = True
            self.buttons_frame.enabled = True
            self.listbox.selected = ()
            self.update_bundle_listbox()
            self.update_selected_bundle()
            self.update_buttons()
            dialog.close()

        t = Thread(target=delete, daemon=True)
        logger.debug(f"Spawning thread {t}")
        t.start()

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
            self.save_last_selected_bundle()

    def load_last_selected_bundle(self):
        """
        Load the last selected bundle.
        """
        if not self.cpybm.data_manager.has_key("last_selected_bundle"):
            return
        last = self.cpybm.data_manager.get_key("last_selected_bundle")
        logger.debug(f"Last selected bundle is {last}")
        if last in self.listbox.values:
            self.listbox.selected = (self.listbox.values.index(last), )
            self.update_selected_bundle()

    def save_last_selected_bundle(self):
        """
        Save the last selected bundle.
        """
        selected = self.listbox.values[self.listbox.selected[0]]
        self.cpybm.data_manager.set_key("last_selected_bundle", selected)

    def make_bundle_listbox(self):
        """
        Make the bundle listbox and scrollbar and stuff.
        """
        self.listbox_frame = Frame(self)
        self.listbox_frame.grid(row=3, column=0, sticky=tk.NSEW)
        self.listbox = Listbox(self.listbox_frame, width=50, height=10,
                               on_select=self.update_buttons)
        self.listbox.grid(row=0, column=0, padx=(1, 0), pady=1, sticky=tk.NSEW)
        self.listbox_scroll = Scrollbar(self.listbox_frame, widget=self.listbox)
        self.listbox_scroll.grid(row=0, column=1, padx=(0, 1), pady=1)
        make_resizable(self.listbox_frame, 0, 0)

    def update_bundle_listbox(self, on_finish: Callable = lambda: None):
        """
        Update the list of bundles available.

        :param on_finish: The function to run when the thread finishes.
        """
        logger.debug("Updating list of bundles")
        self.listbox_frame.enabled = False
        self.buttons_frame.enabled = False
        self.bundles = []

        def update():
            self.cpybm.bundle_manager.index_bundles()
            self.bundles = self.cpybm.bundle_manager.bundles
            self.bundles = sorted(self.bundles, key=lambda b: b.released.timestamp(), reverse=True)
            self.listbox.values = [b.title for b in self.bundles]

            self.listbox_frame.enabled = True
            self.buttons_frame.enabled = True
            self.update_buttons()
            on_finish()

        t = Thread(target=update, daemon=True)
        logger.debug(f"Spawning thread {t}")
        t.start()
