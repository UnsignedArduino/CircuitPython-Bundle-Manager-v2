import logging
from pathlib import Path

from json import loads
import arrow

from helpers.create_logger import create_logger
from helpers.singleton import Singleton

logger = create_logger(name=__name__, level=logging.DEBUG)


class Bundle:
    def __init__(self, path: Path):
        """
        Make a Bundle.

        :param path: The path to the bundle. Inside the directory there should
         be a metadata.json file.
        """
        self.path = path
        self.title = None
        self.tag_name = None
        self.url = None
        self.released = None
        self.bundle_paths = []
        self.versions = []
        self.module_dependencies = {}
        self.load_metadata()

    def load_metadata(self):
        """
        Load the metadata.
        """
        metadata_path = self.path / "metadata.json"
        logger.debug(f"Loading metadata from {metadata_path}")
        metadata = loads(metadata_path.read_text())
        self.title = metadata["title"]
        self.tag_name = metadata["tag_name"]
        self.url = metadata["url"]
        self.released = arrow.get(metadata["released"])
        self.bundle_paths = [Path(p) for p in metadata["bundles"]]
        self.versions = []
        for bundle in self.bundle_paths:
            name = bundle.name
            name = name.replace("adafruit-circuitpython-bundle-", "")
            name = name.replace(f"-{self.tag_name}", "")
            logger.debug(f"Found bundle version: {name}")
            self.versions.append(name)
        self.module_dependencies = metadata["dependencies"]


class BundleManager(metaclass=Singleton):
    def __init__(self, bundle_path: Path):
        """
        Make a BundleManager.

        :param bundle_path: The path to the bundles.
        """
        self.bundle_path = bundle_path
        self.bundles = []
        self.index_bundles()

    def index_bundles(self):
        """
        Search the bundle paths for bundles.
        """
        logger.debug("Indexing bundles...")
        for path in self.bundle_path.glob("*"):
            if not path.is_dir():
                continue
            logger.debug(f"Found bundle {path}")
            self.bundles.append(Bundle(path))
