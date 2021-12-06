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
from typing import Union

from TkZero.Button import Button
from TkZero.Dialog import CustomDialog
from TkZero.Dialog import show_error, show_info
from TkZero.Entry import Entry
from TkZero.Frame import Frame
from TkZero.Label import Label
from TkZero.Listbox import Listbox
from TkZero.Scrollbar import Scrollbar
from github.GithubException import BadCredentialsException

from circuitpython_bundle_manager import CircuitPythonBundleManager
from constants import *
from helpers.create_logger import create_logger
from helpers.resize import make_resizable
from managers.github_manager import GitHubManager
from ui.dialogs.loading import show_download_release

logger = create_logger(name=__name__, level=logging.DEBUG)


class AddBundleDialog(CustomDialog):
    """
    A dialog that shows all the releases you can download.
    """

    def __init__(self, parent, cpybm: CircuitPythonBundleManager,
                 use_community: bool = False):
        """
        Initialize the AddBundleDialog

        :param parent: The parent of this dialog.
        :param cpybm: The CircuitPythonBundleManager instance.
        :param use_community: Whether to use the community bundle repo
        """
        super().__init__(parent)
        self.cpybm = cpybm
        self.use_community = use_community
        self.repo = COMMUNITY_REPO if use_community else BUNDLE_REPO
        logger.debug(f"Using repo {self.repo}")
        logger.debug("Opening add bundle dialog")
        self.title = f"CircuitPython Bundle Manager v2: Select release " \
                     f"from {COMMUNITY_NAME if use_community else BUNDLE_NAME}"
        if not cpybm.cred_manager.has_github_token():
            logger.warning("No token found!")
            show_error(self, title="CircuitPython Bundle Manager v2: Error!",
                       message="No token has been detected! Please go to "
                               "Other --> Go to credential settings --> Open "
                               "credential manager and fill and save a valid "
                               "GitHub token!")
            self.destroy()
            return
        self.token = cpybm.cred_manager.get_github_token()
        self.values = {}
        self.curr_page = 0
        self.max_page = 0
        self.create_gui()
        self.bind("<Escape>", lambda _: self.close())
        self.enabled = False
        self.lift()
        self.focus_force()
        self.grab_focus()
        self.update_idletasks()
        self.after(10, lambda: self.update_first_time())
        self.wait_till_destroyed()

    def make_sidebar(self):
        """
        Make the side bar in the dialog. (With all the buttons)
        """
        button_frame = Frame(self)
        button_frame.grid(row=1, column=1, padx=1, pady=1, sticky=tk.NW + tk.E)
        make_resizable(button_frame, range(0, 4), 0)

        self.open_url_button = Button(button_frame,
                                      text="Open release on GitHub")
        self.open_url_button.enabled = False
        self.open_url_button.grid(row=0, column=0, padx=1, pady=1,
                                  sticky=tk.NW + tk.E)

        version_frame = Frame(button_frame)
        version_frame.grid(row=1, column=0, padx=1, pady=1,
                           sticky=tk.NW + tk.E)
        make_resizable(version_frame, 0, 1)

        self.versions_label = Label(version_frame, text="Versions available: ")
        self.versions_label.grid(row=0, column=0, padx=1, pady=1, sticky=tk.NW)

        self.versions_entry = Entry(version_frame, width=25)
        self.versions_entry.read_only = True
        self.versions_entry.grid(row=0, column=1, padx=1, pady=1,
                                 sticky=tk.NW + tk.E)

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
                              title="CircuitPython Bundle Manager v2: Info",
                              message="Successfully downloaded release!")
                finally:
                    download_dlg.destroy()
                    self.grab_set()

            t = Thread(target=actually_download)
            logger.debug(f"Starting thread {t}")
            t.start()

        self.download_button = Button(button_frame, text="Download",
                                      command=download)
        self.download_button.enabled = False
        self.download_button.grid(row=2, column=0, padx=1, pady=1,
                                  sticky=tk.NW + tk.E)

        self.cancel_button = Button(button_frame, text="Close",
                                    command=self.close)
        self.cancel_button.grid(row=3, column=0, padx=1, pady=1,
                                sticky=tk.NW + tk.E)

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
            show_name = show_name.replace("circuitpython-community-bundle-", "")
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
        listbox_label.grid(row=0, column=0, columnspan=2, padx=1, pady=1,
                           sticky=tk.NW)

        self.listbox = Listbox(listbox_frame, values=list(self.values.keys()),
                               height=10, width=30,
                               on_select=self.update_sidebar)
        self.listbox.grid(row=1, column=0, padx=(1, 0), pady=1, sticky=tk.NSEW)

        listbox_scroll = Scrollbar(listbox_frame, widget=self.listbox)
        listbox_scroll.grid(row=1, column=1, padx=(0, 1), pady=1)

        navigate_frame = Frame(listbox_frame)
        navigate_frame.grid(row=2, column=0, padx=1, pady=1, sticky=tk.NSEW)
        make_resizable(navigate_frame, rows=0, cols=range(6))

        self.leftest_button = Button(navigate_frame, text="<<",
                                     command=lambda: self.change_page(0))
        self.leftest_button.configure(width=3)
        self.leftest_button.grid(row=0, column=0, padx=1, pady=1,
                                 sticky=tk.NW + tk.E)

        self.left_button = Button(navigate_frame, text="<",
                                  command=lambda: self.change_page(
                                      self.curr_page - 1))
        self.left_button.configure(width=3)
        self.left_button.grid(row=0, column=1, padx=1, pady=1,
                              sticky=tk.NW + tk.E)

        self.page_lbl = Label(navigate_frame,
                              text=f"{self.curr_page + 1}/{self.max_page} pages")
        self.page_lbl.grid(row=0, column=3, padx=1, pady=(3, 1),
                           sticky=tk.NW + tk.E)

        self.right_button = Button(navigate_frame, text=">",
                                   command=lambda: self.change_page(
                                       self.curr_page + 1))
        self.right_button.configure(width=3)
        self.right_button.grid(row=0, column=4, padx=1, pady=1,
                               sticky=tk.NW + tk.E)

        self.rightest_button = Button(navigate_frame, text=">>",
                                      command=lambda: self.change_page(
                                          self.max_page - 1))
        self.rightest_button.configure(width=3)
        self.rightest_button.grid(row=0, column=5, padx=1, pady=1,
                                  sticky=tk.NW + tk.E)

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

    def update_first_time(self):
        """
        Update the GUI for the first time.
        """
        self.update_idletasks()
        try:
            self.gm = GitHubManager(self.token, self.repo, BUNDLES_PATH, self.use_community)
        except BadCredentialsException as e:
            logger.exception("Bad token!")
            show_error(self, title="CircuitPython Bundle Manager v2: Error!",
                       message="Bad token! Please go to Other --> Go to "
                               "credential settings --> Open credential "
                               "manager and fill and save a valid GitHub "
                               "token!",
                       detail=str(e))
            self.destroy()
            return
        except Exception as e:
            logger.exception("Error while authenticating with GitHub!")
            show_error(self, title="CircuitPython Bundle Manager v2: Error!",
                       message="Error while authenticating with GitHub!",
                       detail=str(e))
            self.destroy()
            return
        self.max_page = self.gm.max_page
        self.update_page()
        self.enabled = True
        self.update_sidebar()
        self.update_navigation()
        self.update_idletasks()


def add_bundle_dialog(parent, cpybm: CircuitPythonBundleManager,
                      use_community: bool = False):
    """
    Pop up a dialog to guide users on downloading a new bundle.

    :param parent: The parent of this window.
    :param cpybm: The CircuitPythonBundleManager instance.
    :param use_community: Whether to use the community bundle repo or not.
    """
    AddBundleDialog(parent, cpybm, use_community)


def select_bundle_version(parent) -> Union[bool, None]:
    """
    Pop up a dialog for users to select either the regular or community
    bundle.

    :param parent: The parent of this window.
    :return: A bool on whether to use the community version of not, or None if
     canceled.
    """
    dlg = CustomDialog(parent)
    dlg.title = "Select bundle repo"

    make_resizable(dlg, cols=0, rows=range(1, 4))

    select_lbl = Label(dlg, text="Select the bundle repository to use: ")
    select_lbl.grid(row=0, column=0, padx=1, pady=1, sticky=tk.NW)

    def select(use_community):
        dlg.version = use_community
        dlg.close()

    regular_btn = Button(dlg, text=BUNDLE_NAME, command=lambda: select(False))
    regular_btn.grid(row=1, column=0, padx=1, pady=1, sticky=tk.NSEW)
    community_btn = Button(dlg, text=COMMUNITY_NAME, command=lambda: select(True))
    community_btn.grid(row=2, column=0, padx=1, pady=1, sticky=tk.NSEW)
    cancel_btn = Button(dlg, text="Cancel",
                        command=lambda: select(None))
    cancel_btn.grid(row=3, column=0, padx=1, pady=1, sticky=tk.NSEW)

    explanation_lbl = Label(dlg, text="If you are unsure of which on to pick, you probably\n"
                                      "want the Adafruit CircuitPython Bundle. ")
    explanation_lbl.grid(row=4, column=0, padx=1, pady=1, sticky=tk.NSEW)

    dlg.bind("<Escape>", lambda _: dlg.close())
    dlg.lift()
    dlg.focus_force()
    dlg.grab_focus()
    dlg.update_idletasks()
    dlg.wait_till_destroyed()

    try:
        return dlg.version
    except AttributeError:
        return None
