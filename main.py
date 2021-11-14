import logging
from pathlib import Path

from gui import CircuitPythonBundleManagerGUI
from helpers.create_logger import create_logger

logger = create_logger(name=__name__, level=logging.DEBUG)

SETTINGS_PATH = Path.cwd() / "settings.json"
logger.debug(f"Path to settings file is {SETTINGS_PATH}")

gui = CircuitPythonBundleManagerGUI(SETTINGS_PATH)
gui.lift()
logger.debug("Starting event loop")
gui.mainloop()
