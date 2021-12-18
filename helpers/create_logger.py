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

log_location = Path.cwd() / "log.log"


def create_logger(name: str, level: int = logging.DEBUG) -> logging.Logger:
    """
    A simple function to create a logger. You would typically put this right
    under all the other modules you imported.

    And then call `logger.debug()`, `logger.info()`, `logger.warning()`,
    `logger.error()`, `logger.critical()`, and
    `logger.exception` everywhere in that module.

    :param name: A string with the logger name.
    :param level: A integer with the logger level. Defaults to logging.DEBUG.
    :return: A logging.Logger which you can use as a regular logger.
    """
    logger = logging.getLogger(name=name)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level=level)
    file_handler = logging.FileHandler(log_location)
    file_handler.setLevel(level=level)
    formatter = logging.Formatter("%(asctime)s - %(name)s - "
                                  "%(levelname)s - %(message)s")
    console_handler.setFormatter(fmt=formatter)
    file_handler.setFormatter(fmt=formatter)
    logger.propagate = False
    if console_handler not in logger.handlers:
        logger.addHandler(hdlr=console_handler)
    if file_handler not in logger.handlers:
        logger.addHandler(hdlr=file_handler)
    logger.setLevel(level=level)
    logger.debug(f"Created logger named {repr(name)} with level {repr(level)}")
    logger.debug(f"Handlers for {repr(name)}: {repr(logger.handlers)}")
    return logger
