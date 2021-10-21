import logging
from pathlib import Path
from shutil import rmtree

from helpers.operating_system import on_linux, on_macos
from helpers.singleton import Singleton
from managers.bundle_manager import BundleManager, Bundle
from managers.credential_manager import CredentialManager
from managers.device_manager import DeviceManager

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
    def __init__(self, settings: dict):
        self.settings = settings
        self.selected_bundle = None
        self.selected_drive = None
        self.cred_manager = CredentialManager(SERVICE_NAME, GITHUB_TOKEN_NAME)
        self.bundle_manager = BundleManager(BUNDLES_PATH)
        self.device_manager = DeviceManager(DRIVE_PATH)
        self.cached_all_bundles = []

    def delete_bundle(self, bundle: Bundle):
        """
        Delete a bundle.

        :param bundle: A Bundle.
        """
        logging.warning(f"Deleting bundle {bundle}")
        path = bundle.path
        logging.debug(f"Path is {path}")
        rmtree(path)
