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

from pathlib import Path

SETTINGS_PATH = Path.cwd() / "settings.json"
ICON_PATH = Path.cwd() / "icon.png"
LICENSE_PATH = Path.cwd() / "LICENSE"

PROJECT_URL = "https://github.com/UnsignedArduino/CircuitPython-Bundle-Manager-v2"
DOCUMENTATION_URL = "https://github.com/UnsignedArduino/CircuitPython-Bundle-Manager-v2/wiki"
LICENSE_URL = "https://github.com/UnsignedArduino/CircuitPython-Bundle-Manager-v2/blob/main/LICENSE"
