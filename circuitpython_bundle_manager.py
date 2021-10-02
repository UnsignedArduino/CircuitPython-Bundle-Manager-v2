from managers.credential_manager import CredentialManager

SERVICE_NAME = "CircuitPython Bundle Manager v2"
GITHUB_TOKEN_NAME = "github_token"


class BundleManager:
    def __init__(self):
        self.cred_manager = CredentialManager(SERVICE_NAME, GITHUB_TOKEN_NAME)
