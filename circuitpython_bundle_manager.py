from pathlib import Path

from helpers.operating_system import on_linux, on_macos
from helpers.singleton import Singleton
from managers.bundle_manager import BundleManager
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
    def __init__(self):
        self.selected_bundle = None
        self.cred_manager = CredentialManager(SERVICE_NAME, GITHUB_TOKEN_NAME)
        self.bundle_manager = BundleManager(BUNDLES_PATH)
        self.device_manager = DeviceManager(DRIVE_PATH)
