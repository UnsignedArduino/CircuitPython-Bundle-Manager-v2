import logging
import tkinter as tk

from TkZero.Button import Button
from TkZero.Frame import Frame
from TkZero.Labelframe import Labelframe
from TkZero.Notebook import Tab, Notebook

from circuitpython_bundle_manager import CircuitPythonBundleManager
from helpers.create_logger import create_logger
from helpers.resize import make_resizable
from ui.dialogs.credential_dialog import show_credential_manager

logger = create_logger(name=__name__, level=logging.DEBUG)


class OtherTab(Tab):
    """
    The OtherTab.
    """
    def __init__(self, parent: Notebook, cpybm: CircuitPythonBundleManager):
        """
        Make a OtherTab.

        :param parent: The parent of the tab. Should be a
         TkZero.Notebook.Notebook.
        :param cpybm: The CircuitPythonBundleManager instance.
        """
        super().__init__(parent, "Other")
        self.cpybm = cpybm
        logger.debug("Making other tab")
        self.make_gui()

    def make_gui(self):
        """
        Make the GUI for this tab.
        """
        logger.debug("Making GUI")
        self.make_main_frame()
        self.make_credentials_frame()
        make_resizable(self, 0, 0)
        self.hide_main_frame()
        self.show_main_frame()

    def make_main_frame(self):
        """
        Make the main frame contents.
        """
        self.main_frame = Frame(self)
        make_resizable(self.main_frame, 0, 0)
        self.cred_frame_button = Button(self.main_frame, text="Go to credential settings",
                                        command=self.show_credentials_frame)
        self.cred_frame_button.grid(row=0, column=0, padx=1, pady=1, sticky=tk.NW + tk.E)

    def show_main_frame(self):
        """
        Show the main frame.
        """
        self.main_frame.grid(row=0, column=0, padx=1, pady=1, sticky=tk.NSEW)

    def hide_main_frame(self):
        """
        Hide the main frame.
        """
        self.main_frame.grid_forget()

    def make_credentials_frame(self):
        """
        Make the credentials frame contents.
        """
        self.cred_frame = Frame(self)
        make_resizable(self.cred_frame, 0, 0)
        actual_cred_frame = Labelframe(self.cred_frame, text="Credential settings")
        actual_cred_frame.grid(row=0, column=0, padx=1, pady=1, sticky=tk.NSEW)
        make_resizable(actual_cred_frame, 0, 0)
        open_cred_manager_button = Button(actual_cred_frame, text="Open credential manager",
                                          command=lambda: show_credential_manager(self, self.cpybm.cred_manager))
        open_cred_manager_button.grid(row=0, column=0, padx=1, pady=1, sticky=tk.NW + tk.E)
        go_back_button = Button(self.cred_frame, text="Go back to main settings",
                                command=self.hide_credentials_frame)
        go_back_button.grid(row=1, column=0, padx=1, pady=1, sticky=tk.SW + tk.E)

    def show_credentials_frame(self):
        """
        Show the credentials frame.
        """
        self.hide_main_frame()
        self.cred_frame.grid(row=0, column=0, padx=1, pady=1, sticky=tk.NSEW)

    def hide_credentials_frame(self):
        """
        Hide the credentials frame.
        """
        self.cred_frame.grid_forget()
        self.show_main_frame()
