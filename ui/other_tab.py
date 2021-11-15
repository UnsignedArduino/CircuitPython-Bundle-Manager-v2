import logging
from typing import Callable
import tkinter as tk
import webbrowser
from pathlib import Path

from TkZero.Button import Button
from TkZero.Frame import Frame
from TkZero.Labelframe import Labelframe
from TkZero.Notebook import Tab, Notebook

from circuitpython_bundle_manager import CircuitPythonBundleManager
from helpers.create_logger import create_logger
from helpers.resize import make_resizable
from ui.dialogs.credential_dialog import show_credential_manager

logger = create_logger(name=__name__, level=logging.DEBUG)

PROJECT_URL = "https://github.com/UnsignedArduino/CircuitPython-Bundle-Manager-v2"
DOCUMENTATION_URL = "https://github.com/UnsignedArduino/CircuitPython-Bundle-Manager-v2/wiki"


class OtherTab(Tab):
    """
    The OtherTab.
    """
    def __init__(self, parent: Notebook, cpybm: CircuitPythonBundleManager,
                 settings_path: Path):
        """
        Make a OtherTab.

        :param parent: The parent of the tab. Should be a
         TkZero.Notebook.Notebook.
        :param cpybm: The CircuitPythonBundleManager instance.
        :param settings_path: The path to the settings file.
        """
        super().__init__(parent, "Other")
        self.settings_path = settings_path
        self.cpybm = cpybm
        logger.debug("Making other tab")
        self.switching_buttons = []
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
        self.bind_all("<KeyPress-Shift_L>", lambda _: self.on_shift())
        self.bind_all("<KeyPress-Shift_R>", lambda _: self.on_shift())
        self.bind_all("<KeyRelease-Shift_L>", lambda _: self.off_shift())
        self.bind_all("<KeyRelease-Shift_R>", lambda _: self.off_shift())

    def on_shift(self):
        """
        Update some buttons to change behavior on shift key pressed.
        """
        for button in self.switching_buttons:
            button.text = button.other_text
            button.configure(command=button.other_command)

    def off_shift(self):
        """
        Update some buttons to change behavior on shift key released.
        """
        for button in self.switching_buttons:
            button.text = button.regular_text
            button.configure(command=button.regular_command)

    def copy_to_clipboard(self, text: str):
        """
        Copy something to the clipboard.

        :param text: The text to copy.
        """
        self.clipboard_clear()
        self.clipboard_append(text)

    def make_switching_button(self, parent, text: str, command: Callable,
                              other_text: str, other_command: Callable) -> Button:
        """
        Make a button that switches behaviors when the shift key is pressed.

        :param parent: The parent of the button.
        :param text: Text when shift isn't pressed.
        :param command: Command when shift isn't pressed.
        :param other_text: Text when shift is pressed.
        :param other_command: Command when shift is pressed.
        :return: A TkZero.Button.Button
        """
        button = Button(parent, text=text, command=command)
        button.regular_text = text
        button.regular_command = command
        button.other_text = other_text
        button.other_command = other_command
        self.switching_buttons.append(button)
        return button

    def make_main_frame(self):
        """
        Make the main frame contents.
        """
        self.main_frame = Frame(self)
        make_resizable(self.main_frame, 0, 0)
        self.cred_frame_button = Button(self.main_frame, text="Go to credential settings",
                                        command=self.show_credentials_frame)
        self.cred_frame_button.grid(row=0, column=0, padx=1, pady=1, sticky=tk.NW + tk.E)
        self.open_project_button = self.make_switching_button(
            parent=self.main_frame,
            text="Open project on GitHub",
            command=lambda: webbrowser.open(PROJECT_URL),
            other_text="Copy URL to project on GitHub",
            other_command=lambda: self.copy_to_clipboard(PROJECT_URL)
        )
        self.open_project_button.grid(row=1, column=0, padx=1, pady=1, sticky=tk.SW + tk.E)
        self.open_docs_button = self.make_switching_button(
            parent=self.main_frame,
            text="Open documentation online in default browser",
            command=lambda: webbrowser.open(DOCUMENTATION_URL),
            other_text="Copy URL to online documentation",
            other_command=lambda: self.copy_to_clipboard(DOCUMENTATION_URL)
        )
        self.open_docs_button.grid(row=2, column=0, padx=1, pady=1, sticky=tk.SW + tk.E)
        self.open_json_button = self.make_switching_button(
            parent=self.main_frame,
            text="Open settings file in default JSON application",
            command=lambda: webbrowser.open(str(self.settings_path)),
            other_text="Copy path to settings file to clipboard",
            other_command=lambda: self.copy_to_clipboard(str(self.settings_path))
        )
        self.open_json_button.grid(row=3, column=0, padx=1, pady=1, sticky=tk.SW + tk.E)

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
