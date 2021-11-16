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

from constants import *
from gui import CircuitPythonBundleManagerGUI
from TkZero.Dialog import show_error
from helpers.create_logger import create_logger

logger = create_logger(name=__name__, level=logging.DEBUG)

logger.debug(f"Path to settings file is {SETTINGS_PATH}")

gui = CircuitPythonBundleManagerGUI(SETTINGS_PATH)
try:
    gui.lift()
    logger.debug("Starting event loop")
    gui.mainloop()
except Exception as e:
    show_error(gui, title="CircuitPython Bundle Manager: Error!",
               message=f"Fatel error encountered!",
               detail=str(e))
