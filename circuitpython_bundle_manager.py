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
from shutil import rmtree

from constants import *
from helpers.singleton import Singleton
from managers.bundle_manager import BundleManager, Bundle
from managers.credential_manager import CredentialManager
from managers.data_manager import DataManager
from managers.device_manager import DeviceManager
from managers.device_manager import Drive


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
