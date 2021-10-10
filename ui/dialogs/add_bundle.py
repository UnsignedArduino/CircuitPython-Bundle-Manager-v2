import logging
import tkinter as tk
import webbrowser
from threading import Thread

from TkZero.Button import Button
from TkZero.Dialog import CustomDialog
from TkZero.Entry import Entry
from TkZero.Frame import Frame
from TkZero.Label import Label
from TkZero.Listbox import Listbox
from TkZero.Scrollbar import Scrollbar
from github import GitRelease
from TkZero.Dialog import show_error, show_info

from circuitpython_bundle_manager import CircuitPythonBundleManager, \
    BUNDLE_REPO, BUNDLES_PATH
from managers.github_manager import GitHubManager
from helpers.create_logger import create_logger
from helpers.resize import make_resizable
from managers.github_manager import GitHubManager
from ui.dialogs.loading import show_get_releases, show_download_release

logger = create_logger(name=__name__, level=logging.DEBUG)


class NoTokenError(Exception):
    """No token has been detected in the OS' keyring"""


def make_release_select_frame(gm: GitHubManager,
                              parent, releases: list[GitRelease]) -> Frame:
    """
    Make the release select frame and wait until the user selects one

    :param gm: A GitHub manager already initialized.
    :param parent: The parent.
    :param releases: A list of GitReleases.
    :return: The frame everything was in.
    """
    frame = Frame(parent)
    frame.grid(row=0, column=0, padx=1, pady=1, sticky=tk.NSEW)
    make_resizable(frame, 1, range(0, 2))

    listbox_frame = Frame(frame)
    listbox_frame.grid(row=1, column=0, padx=1, pady=1, sticky=tk.NSEW)
    make_resizable(listbox_frame, 1, 0)

    listbox_label = Label(frame, text="Available releases:")
    listbox_label.grid(row=0, column=0, columnspan=2, padx=1, pady=1, sticky=tk.NW)

    values = {}
    for release in releases:
        values[release.title] = release

    def update():
        open_url_button.enabled = False
        versions_label.enabled = False
        versions_entry.enabled = True
        versions_entry.read_only = False
        versions_entry.value = ""
        versions_entry.read_only = True
        versions_entry.enabled = False
        download_button.enabled = False
        parent.update_idletasks()
        if len(listbox.selected) == 0:
            return
        selected_index = listbox.selected[0]
        selected = values[list(values.keys())[selected_index]].title
        selected_release = values[selected]
        open_url_button.configure(
            command=lambda: webbrowser.open(selected_release.html_url)
        )
        assets = list(selected_release.get_assets())
        versions_entry.enabled = True
        versions_entry.read_only = False
        versions = []
        for asset in assets:
            name = asset.name
            if "-mpy-" not in name and "-py-" not in name:
                continue
            show_name = name.replace("adafruit-circuitpython-bundle-", "")
            show_name = show_name.replace(f"-{selected_release.tag_name}.zip", "")
            versions.append(show_name)
        versions_entry.value = ", ".join(versions)
        versions_entry.read_only = True
        open_url_button.enabled = True
        versions_label.enabled = True
        download_button.enabled = True

    listbox = Listbox(listbox_frame, values=list(values.keys()),
                      height=10, width=30, on_select=update)
    listbox.grid(row=1, column=0, padx=(1, 0), pady=1, sticky=tk.NSEW)

    listbox_scroll = Scrollbar(listbox_frame, widget=listbox)
    listbox_scroll.grid(row=1, column=1, padx=(0, 1), pady=1)

    button_frame = Frame(frame)
    button_frame.grid(row=1, column=1, padx=1, pady=1, sticky=tk.NW + tk.E)
    make_resizable(button_frame, range(0, 4), 0)

    open_url_button = Button(button_frame, text="Open release on GitHub")
    open_url_button.enabled = False
    open_url_button.grid(row=0, column=0, padx=1, pady=1, sticky=tk.NW + tk.E)

    version_frame = Frame(button_frame)
    version_frame.grid(row=1, column=0, padx=1, pady=1, sticky=tk.NW + tk.E)
    make_resizable(version_frame, 0, 1)

    versions_label = Label(version_frame, text="Versions available: ")
    versions_label.grid(row=0, column=0, padx=1, pady=1, sticky=tk.NW)

    versions_entry = Entry(version_frame, width=25)
    versions_entry.read_only = True
    versions_entry.grid(row=0, column=1, padx=1, pady=1, sticky=tk.NW + tk.E)

    def download():
        download_dlg = show_download_release(parent)

        def actually_download():
            selected_index = listbox.selected[0]
            selected = values[list(values.keys())[selected_index]].title
            selected_release = values[selected]
            try:
                gm.download_release(selected_release)
            except Exception as e:
                logger.exception("Error while downloading release!")
                show_error(parent, title="CircuitPython Bundle Manager v2: Error!",
                           message="There was an error downloading the release!",
                           detail=str(e))
            else:
                show_info(parent, title="CircuitPython Bundle Manager v2: Error!",
                           message="Successfully downloaded release!")
            finally:
                download_dlg.close()

        t = Thread(target=actually_download)
        logger.debug(f"Starting thread {t}")
        t.start()

    download_button = Button(button_frame, text="Download",
                             command=download)
    download_button.enabled = False
    download_button.grid(row=2, column=0, padx=1, pady=1, sticky=tk.NW + tk.E)

    cancel_button = Button(button_frame, text="Close",
                           command=parent.close)
    cancel_button.grid(row=3, column=0, padx=1, pady=1, sticky=tk.NW + tk.E)
    return frame


def add_bundle_dialog(parent, cpybm: CircuitPythonBundleManager):
    """
    Pop up a dialog to guide users on downloading a new bundle.

    :param parent: The parent of this window.
    :param cpybm: The CircuitPythonBundleManager instance.
    """
    if not cpybm.cred_manager.has_github_token():
        raise NoTokenError("No token has been detected! "
                           "Please go to Other --> Go to credential settings "
                           "--> Open credential manager and fill and save a "
                           "valid GitHub token!")

    dialog = CustomDialog(parent)
    logger.debug("Opening add bundle dialog")
    dialog.title = f"CircuitPython Bundle Manager v2: Add bundle"

    make_resizable(dialog, 0, 0)

    token = cpybm.cred_manager.get_github_token()
    gm = GitHubManager(token, BUNDLE_REPO, BUNDLES_PATH)
    fake_frame = make_release_select_frame(gm, dialog, [])

    loading, pb = show_get_releases(dialog)

    def update_pb(got, total):
        pb.value = got
        pb.maximum = total

    def get_and_select_release():
        if len(cpybm.cached_all_bundles) == 0:
            logger.debug("Did not find release list in memory cache, downloading list")
            releases = gm.get_bundle_releases(update_pb)
            cpybm.cached_all_bundles = releases
        else:
            logger.debug(f"Found {len(cpybm.cached_all_bundles)} releases in memory cache")
            releases = cpybm.cached_all_bundles
        loading.close()
        fake_frame.grid_forget()
        make_release_select_frame(gm, dialog, releases)

    t = Thread(target=get_and_select_release, daemon=True)
    logger.debug(f"Starting thread {t}")
    t.start()

    dialog.wait_till_destroyed()
