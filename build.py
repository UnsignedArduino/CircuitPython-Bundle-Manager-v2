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
from shutil import rmtree, copy2, copytree
from subprocess import run

required = [
    "icon.png",
    "circuitpython_bundle_manager.py",
    "constants.py",
    "gui.py",
    "main.py",
    "LICENSE",
    "helpers",
    "managers",
    "ui"
]

required = [Path().cwd() / name for name in required]

print("To be included in zipapp:")

for path in required:
    assert path.exists()
    if path.is_file():
        print("    " + str(path))
    else:
        print("  * " + str(path))

output_path = Path.cwd() / "dist"
output_path.mkdir(parents=True, exist_ok=True)

app_output_path = output_path / "CircuitPython_Bundle_Manager_v2"
if app_output_path.exists():
    rmtree(app_output_path)
app_output_path.mkdir(parents=True)

print(f"Copying files to {str(app_output_path)}")

for path in required:
    if path.is_file():
        copy2(path, app_output_path)
    else:
        copytree(path, app_output_path / path.name)

requirements_path = Path.cwd() / "requirements.txt"
print(f"Using requirements file from {str(requirements_path)}")

pip_cmd = f"pip install -r \"{str(requirements_path)}\" " \
          f"--target \"{str(app_output_path)}\""
print(f"Running \"{pip_cmd}\"")

run(pip_cmd, shell=True)

zip_output_path = output_path / "CircuitPython_Bundle_Manager_v2.zip"
print(f"Writing zipapp to {str(zip_output_path)}")

zipapp_cmd = f"python -m zipapp \"{str(app_output_path)}\" " \
             f"-o \"{str(zip_output_path)}\" " \
             f"-m \"main:main\" " \
             f"-c"
print(f"Running \"{zipapp_cmd}\"")

run(zipapp_cmd, shell=True)
