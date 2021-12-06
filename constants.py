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
from helpers.operating_system import on_linux, on_macos

BUNDLES_PATH = Path.cwd() / "bundles"
if on_linux():
    DRIVE_PATH = Path("/media")
elif on_macos():
    DRIVE_PATH = Path("/Volumes")
else:
    DRIVE_PATH = None
SETTINGS_PATH = Path.cwd() / "settings.json"
ICON_PATH = Path.cwd() / "icon.png"
LICENSE_PATH = Path.cwd() / "LICENSE"

PROJECT_URL = "https://github.com/UnsignedArduino/CircuitPython-Bundle-Manager-v2"
DOCUMENTATION_URL = "https://github.com/UnsignedArduino/CircuitPython-Bundle-Manager-v2/wiki"
ISSUE_URL = "https://github.com/UnsignedArduino/CircuitPython-Bundle-Manager-v2/issues"
LICENSE_URL = "https://github.com/UnsignedArduino/CircuitPython-Bundle-Manager-v2/blob/main/LICENSE"

SERVICE_NAME = "CircuitPython Bundle Manager v2"
GITHUB_TOKEN_NAME = "github_token"
BUNDLE_REPO = "adafruit/Adafruit_CircuitPython_Bundle"

