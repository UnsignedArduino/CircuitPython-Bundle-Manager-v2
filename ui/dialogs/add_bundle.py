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
import webbrowser
from threading import Thread

from TkZero.Button import Button
from TkZero.Dialog import CustomDialog
from TkZero.Dialog import show_error, show_info
from TkZero.Entry import Entry
from TkZero.Frame import Frame
from TkZero.Label import Label
from TkZero.Listbox import Listbox
from TkZero.Scrollbar import Scrollbar

from circuitpython_bundle_manager import CircuitPythonBundleManager, \
    BUNDLE_REPO, BUNDLES_PATH
from helpers.create_logger import create_logger
from helpers.resize import make_resizable
from managers.github_manager import GitHubManager
from ui.dialogs.loading import show_download_release

logger = create_logger(name=__name__, level=logging.DEBUG)


class NoTokenError(Exception):
    """No token has been detected in the OS' keyring"""


class AddBundleDialog(CustomDialog):
    """
    A dialog that shows all the releases you can download.
    """
    def __init__(self, parent, cpybm: CircuitPythonBundleManager):
        """
        Initialize the AddBundleDialog

        :param parent: The parent of this dialog.
        :param cpybm: The CircuitPythonBundleManager instance.
        """
        super().__init__(parent)
        self.cpybm = cpybm
        logger.debug("Opening add bundle dialog")
        self.title = "CircuitPython Bundle Manager v2: Add bundle"
        self.token = cpybm.cred_manager.get_github_token()
        self.gm = GitHubManager(self.token, BUNDLE_REPO, BUNDLES_PATH)
        self.values = {}
        self.curr_page = 0
        self.max_page = self.gm.max_page
        self.create_gui()
        self.grab_set()
        self.wait_till_destroyed()
        self.grab_release()

    def make_sidebar(self):
        """
        Make the side bar in the dialog. (With all the buttons)
        """
        button_frame = Frame(self)
        button_frame.grid(row=1, column=1, padx=1, pady=1, sticky=tk.NW + tk.E)
        make_resizable(button_frame, range(0, 4), 0)

        self.open_url_button = Button(button_frame, text="Open release on GitHub")
        self.open_url_button.enabled = False
        self.open_url_button.grid(row=0, column=0, padx=1, pady=1, sticky=tk.NW + tk.E)

        version_frame = Frame(button_frame)
        version_frame.grid(row=1, column=0, padx=1, pady=1, sticky=tk.NW + tk.E)
        make_resizable(version_frame, 0, 1)

        self.versions_label = Label(version_frame, text="Versions available: ")
        self.versions_label.grid(row=0, column=0, padx=1, pady=1, sticky=tk.NW)

        self.versions_entry = Entry(version_frame, width=25)
        self.versions_entry.read_only = True
        self.versions_entry.grid(row=0, column=1, padx=1, pady=1, sticky=tk.NW + tk.E)

        def download():
            download_dlg, pb, lbl = show_download_release(self)

            def update_pb(got, total, status):
                pb.value = got
                pb.maximum = total
                lbl.text = status

            def actually_download():
                selected_index = self.listbox.selected[0]
                selected = self.values[
                    list(self.values.keys())[selected_index]].title
                selected_release = self.values[selected]
                try:
                    self.gm.download_release(selected_release, update_pb)
                except Exception as e:
                    logger.exception("Error while downloading release!")
                    show_error(self,
                               title="CircuitPython Bundle Manager v2: Error!",
                               message="There was an error downloading the release!",
                               detail=str(e))
                else:
                    show_info(self,
                              title="CircuitPython Bundle Manager v2: Error!",
                              message="Successfully downloaded release!")
                finally:
                    download_dlg.destroy()
                    self.grab_set()

            t = Thread(target=actually_download)
            logger.debug(f"Starting thread {t}")
            t.start()

        self.download_button = Button(button_frame, text="Download", command=download)
        self.download_button.enabled = False
        self.download_button.grid(row=2, column=0, padx=1, pady=1, sticky=tk.NW + tk.E)

        self.cancel_button = Button(button_frame, text="Close", command=self.close)
        self.cancel_button.grid(row=3, column=0, padx=1, pady=1, sticky=tk.NW + tk.E)

    def update_sidebar(self):
        """
        Update the side bar in the dialog. (With all the buttons)
        """
        logger.debug("Update sidebar")
        self.open_url_button.enabled = False
        self.versions_label.enabled = False
        self.versions_entry.enabled = True
        self.versions_entry.read_only = False
        self.versions_entry.value = ""
        self.versions_entry.read_only = True
        self.versions_entry.enabled = False
        self.download_button.enabled = False
        self.update_idletasks()
        if len(self.listbox.selected) == 0:
            return
        selected_index = self.listbox.selected[0]
        selected = self.values[list(self.values.keys())[selected_index]].title
        selected_release = self.values[selected]
        self.open_url_button.configure(
            command=lambda: webbrowser.open(selected_release.html_url)
        )
        assets = list(selected_release.get_assets())
        self.versions_entry.enabled = True
        self.versions_entry.read_only = False
        versions = []
        for asset in assets:
            name = asset.name
            if "-mpy-" not in name and "-py-" not in name:
                continue
            show_name = name.replace("adafruit-circuitpython-bundle-", "")
            show_name = show_name.replace(
                f"-{selected_release.tag_name}.zip", "")
            versions.append(show_name)
        self.versions_entry.value = ", ".join(versions)
        self.versions_entry.read_only = True
        self.open_url_button.enabled = True
        self.versions_label.enabled = True
        self.download_button.enabled = True

    def change_page(self, new_page: int):
        """
        Set the new page.

        :param new_page: The new page to set.
        """
        self.curr_page = new_page
        self.update_navigation()
        self.update_page()

    def make_listbox(self):
        """
        Make the listbox which has all the releases in it.
        """
        listbox_frame = Frame(self)
        listbox_frame.grid(row=1, column=0, padx=1, pady=1, sticky=tk.NSEW)
        make_resizable(listbox_frame, range(1, 2), 0)

        listbox_label = Label(self, text="Available releases:")
        listbox_label.grid(row=0, column=0, columnspan=2, padx=1, pady=1, sticky=tk.NW)

        self.listbox = Listbox(listbox_frame, values=list(self.values.keys()),
                               height=10, width=30, on_select=self.update_sidebar)
        self.listbox.grid(row=1, column=0, padx=(1, 0), pady=1, sticky=tk.NSEW)

        listbox_scroll = Scrollbar(listbox_frame, widget=self.listbox)
        listbox_scroll.grid(row=1, column=1, padx=(0, 1), pady=1)

        navigate_frame = Frame(listbox_frame)
        navigate_frame.grid(row=2, column=0, padx=1, pady=1, sticky=tk.NSEW)
        make_resizable(navigate_frame, rows=0, cols=range(6))

        self.leftest_button = Button(navigate_frame, text="<<", command=lambda: self.change_page(0))
        self.leftest_button.configure(width=3)
        self.leftest_button.grid(row=0, column=0, padx=1, pady=1, sticky=tk.NW + tk.E)

        self.left_button = Button(navigate_frame, text="<", command=lambda: self.change_page(self.curr_page - 1))
        self.left_button.configure(width=3)
        self.left_button.grid(row=0, column=1, padx=1, pady=1, sticky=tk.NW + tk.E)

        self.page_lbl = Label(navigate_frame, text=f"{self.curr_page + 1}/{self.max_page} pages")
        self.page_lbl.grid(row=0, column=3, padx=1, pady=(3, 1), sticky=tk.NW + tk.E)

        self.right_button = Button(navigate_frame, text=">", command=lambda: self.change_page(self.curr_page + 1))
        self.right_button.configure(width=3)
        self.right_button.grid(row=0, column=4, padx=1, pady=1, sticky=tk.NW + tk.E)

        self.rightest_button = Button(navigate_frame, text=">>", command=lambda: self.change_page(self.max_page - 1))
        self.rightest_button.configure(width=3)
        self.rightest_button.grid(row=0, column=5, padx=1, pady=1, sticky=tk.NW + tk.E)

    def update_navigation(self):
        """
        Update the navigation
        """
        logger.debug("Updating navigation")
        if self.curr_page == 0:
            self.left_button.enabled = False
            self.leftest_button.enabled = False
        else:
            self.left_button.enabled = True
            self.leftest_button.enabled = True
        if self.curr_page == self.max_page - 1:
            self.right_button.enabled = False
            self.rightest_button.enabled = False
        else:
            self.right_button.enabled = True
            self.rightest_button.enabled = True
        self.page_lbl.text = f"{self.curr_page + 1}/{self.max_page} pages"

    def update_page(self):
        """
        Update the current page
        """
        logger.debug("Updating current page")
        self.enabled = False
        self.update_idletasks()
        self.values = {}
        logger.debug(f"Updating to page {self.curr_page}")
        for release in self.gm.release_pag.get_page(self.curr_page):
            self.values[release.title] = release
        self.listbox.values = self.values.keys()
        self.enabled = True
        self.update_sidebar()
        self.update_navigation()

    def create_gui(self):
        """
        Create the GUI for this dialog.
        """
        self.make_listbox()
        self.make_sidebar()
        self.update_sidebar()
        self.update_navigation()
        self.update_page()


def add_bundle_dialog(parent, cpybm: CircuitPythonBundleManager):
    """
    Pop up a dialog to guide users on downloading a new bundle.

    :param parent: The parent of this window.
    :param cpybm: The CircuitPythonBundleManager instance.
    """
    if not cpybm.cred_manager.has_github_token():
        raise NoTokenError("No token has been detected! Please go to "
                           "Other --> Go to credential settings --> Open "
                           "credential manager and fill and save a valid "
                           "GitHub token!")
    try:
        dlg = AddBundleDialog(parent, cpybm)
    finally:
        dlg.destroy()
