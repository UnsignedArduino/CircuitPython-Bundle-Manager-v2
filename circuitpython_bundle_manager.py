from pathlib import Path

from helpers.singleton import Singleton
from managers.credential_manager import CredentialManager

SERVICE_NAME = "CircuitPython Bundle Manager v2"
GITHUB_TOKEN_NAME = "github_token"
BUNDLE_REPO = "adafruit/Adafruit_CircuitPython_Bundle"
BUNDLES_PATH = Path.cwd() / "bundles"


class BundleManager(metaclass=Singleton):
    def __init__(self):
        self.cred_manager = CredentialManager(SERVICE_NAME, GITHUB_TOKEN_NAME)
