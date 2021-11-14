import logging
from pathlib import Path
from shutil import rmtree

from helpers.operating_system import on_linux, on_macos
from helpers.singleton import Singleton
from managers.bundle_manager import BundleManager, Bundle
from managers.credential_manager import CredentialManager
from managers.device_manager import DeviceManager
from managers.device_manager import Drive
from managers.data_manager import DataManager

SERVICE_NAME = "CircuitPython Bundle Manager v2"
GITHUB_TOKEN_NAME = "github_token"
BUNDLE_REPO = "adafruit/Adafruit_CircuitPython_Bundle"
BUNDLES_PATH = Path.cwd() / "bundles"
if on_linux():
    DRIVE_PATH = Path("/media")
elif on_macos():
    DRIVE_PATH = Path("/Volumes")
else:
    DRIVE_PATH = None


class CircuitPythonBundleManager(metaclass=Singleton):
    def __init__(self, settings_path: Path):
        self._selected_bundle = None
        self.on_new_selected_bundle = lambda: None
        self._selected_drive = None
        self.on_new_selected_drive = lambda: None
        self.cred_manager = CredentialManager(SERVICE_NAME, GITHUB_TOKEN_NAME)
        self.bundle_manager = BundleManager(BUNDLES_PATH)
        self.device_manager = DeviceManager(DRIVE_PATH)
        self.data_manager = DataManager(settings_path)

    def delete_bundle(self, bundle: Bundle):
        """
        Delete a bundle.

        :param bundle: A Bundle.
        """
        logging.warning(f"Deleting bundle {bundle}")
        path = bundle.path
        logging.debug(f"Path is {path}")
        rmtree(path)

    @property
    def selected_bundle(self) -> Bundle:
        """
        Get the currently selected bundle.

        :return: A Bundle.
        """
        return self._selected_bundle

    @selected_bundle.setter
    def selected_bundle(self, new_bundle: Bundle):
        """
        Set the currently selected bundle.

        :param new_bundle: A Bundle.
        """
        self._selected_bundle = new_bundle
        self.on_new_selected_bundle()

    @property
    def selected_drive(self) -> Drive:
        """
        Get the currently selected bundle.

        :return: A Drive.
        """
        return self._selected_drive

    @selected_drive.setter
    def selected_drive(self, new_drive: Drive):
        """
        Set the currently selected bundle.

        :param new_drive: A Drive.
        """
        self._selected_drive = new_drive
        self.on_new_selected_drive()
