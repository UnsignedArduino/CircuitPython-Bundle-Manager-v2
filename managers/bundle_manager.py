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
from pathlib import Path

from json import loads
import arrow

from helpers.create_logger import create_logger
from helpers.singleton import Singleton

logger = create_logger(name=__name__, level=logging.DEBUG)


class Module:
    def __init__(self, path: Path, data: dict):
        """
        Make a Module.

        :param path: The path to the module. Can be either a single file or a
         directory. (package)
        :param data: A dictionary containing the dependencies for all modules.
        """
        self.path = path
        self.name = path.name
        if len(data) > 0:
            self.is_package = data[self.path.stem]["package"]
            self.pypi_name = data[self.path.stem]["pypi_name"]
            self.version = data[self.path.stem]["version"]
            self.repo = data[self.path.stem]["repo"]
            self.dependencies = []
            for dependency in data[self.path.stem]["dependencies"]:
                self.dependencies.append(
                    Module(self.path.parent / dependency, data)
                )
        else:
            self.is_package = None
            self.pypi_name = None
            self.version = None
            self.repo = None
            self.dependencies = []


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
        self.bundle = {}
        self.load_metadata()
        self.load_modules()

    def load_modules(self):
        """
        Load the modules in the bundle.
        """
        logger.debug("Loading modules")
        for bundle in self.bundle_paths:
            version = bundle.name
            version = version.replace("adafruit-circuitpython-bundle-", "")
            version = version.replace("circuitpython-community-bundle-", "")
            version = version.replace(f"-{self.tag_name}", "")
            modules_path = bundle / "lib"
            logger.debug(f"Found {len(list(modules_path.glob('*')))} modules "
                         f"in {version} version")
            modules = {}
            for path in modules_path.glob("*"):
                modules[path.name] = Module(path, self.module_dependencies)
            self.bundle[version] = modules

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
            name = name.replace("circuitpython-community-bundle-", "")
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
        self.bundles = []
        for path in self.bundle_path.glob("*"):
            if not path.is_dir():
                continue
            logger.debug(f"Found bundle {path}")
            try:
                b = Bundle(path)
            except FileNotFoundError:
                logger.exception(f"Skipping over bundle at {path}")
            else:
                self.bundles.append(b)
