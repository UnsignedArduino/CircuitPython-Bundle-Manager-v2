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
from json import dumps, loads
from pathlib import Path
from typing import Hashable

from helpers.create_logger import create_logger
from helpers.singleton import Singleton

logger = create_logger(name=__name__, level=logging.DEBUG)


class DataManager(metaclass=Singleton):
    def __init__(self, data_path: Path):
        """
        Make a DataManager.

        :param data_path: The path to the JSON file where the information
         is stored.
        """
        self.path = data_path
        self.dict = {}
        self.load_from_disk()

    def load_from_disk(self):
        """
        Reload the data from the disk.
        """
        logger.debug(f"Loading data from {self.path}")
        if not self.path.exists():
            self.path.write_text("{}")
        self.dict = loads(self.path.read_text())

    def save_to_disk(self):
        """
        Save the data to the disk.
        """
        logger.debug(f"Saving data to {self.path}")
        self.path.write_text(dumps(self.dict, indent=2, sort_keys=True))

    def set_key(self, key: str, value: Hashable):
        """
        Set a key to a value in the data.

        :param key: The key as a string.
        :param value: A Hashable object.
        """
        if key in self.dict and self.dict[key] == value:
            return
        self.dict[key] = value
        self.save_to_disk()

    def get_key(self, key: str) -> Hashable:
        """
        Get a key from the data.

        :param key: The key as a string.
        :return: The Hashable object.
        """
        return self.dict[key]

    def has_key(self, key: str) -> bool:
        """
        Check whether a key exists.

        :param key: The key as a string.
        :return: A boolean on whether the key exists or not.
        """
        return key in self.dict

    def del_key(self, key: str):
        """
        Delete a key.

        :param key: The key as a string.
        """
        del self.dict[key]
