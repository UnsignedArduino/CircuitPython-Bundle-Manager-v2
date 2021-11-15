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
from sys import platform

from helpers.create_logger import create_logger

logger = create_logger(name=__name__, level=logging.DEBUG)

WINDOWS = "win32"
MACOS = "darwin"
LINUX = "linux"

logger.debug(f"OS is {platform}")


def on_windows() -> bool:
    """
    Returns whether we are on Windows or not.

    :return: A bool.
    """
    return platform == WINDOWS


def on_macos() -> bool:
    """
    Returns whether we are on macOS or not.

    :return: A bool.
    """
    return platform == MACOS


def on_linux() -> bool:
    """
    Returns whether we are on Linux or not.

    :return: A bool.
    """
    return platform == LINUX
