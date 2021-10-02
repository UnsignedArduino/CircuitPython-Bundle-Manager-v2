import logging
import re

from helpers.create_logger import create_logger

logger = create_logger(name=__name__, level=logging.DEBUG)


def filename_sanitize(filename: str) -> str:
    """
    Sanitize a filename. Found https://stackoverflow.com/a/13593932/10291933

    :param filename: A string.
    :return: A string.
    """
    return re.sub("[^\w\-_\. ]", "_", filename)


def directory_sanitize(filename: str) -> str:
    """
    Sanitize a directory. Found https://stackoverflow.com/a/13593932/10291933

    :param filename: A string.
    :return: A string.
    """
    return re.sub("[^\w\-_\. ]", "_", filename).replace(".", "_")