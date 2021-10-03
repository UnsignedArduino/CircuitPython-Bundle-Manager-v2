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
