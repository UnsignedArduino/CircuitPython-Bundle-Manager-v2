import logging
from pathlib import Path
from json import loads, dumps

from gui import CircuitPythonBundleManagerGUI
from helpers.create_logger import create_logger

logger = create_logger(name=__name__, level=logging.DEBUG)

SETTINGS_PATH = Path.cwd() / "settings.json"
logger.debug(f"Path to settings file is {SETTINGS_PATH}")
if not SETTINGS_PATH.exists():
    logger.warning(f"Settings file does not exist, creating!")
    SETTINGS_PATH.write_text(dumps({}, indent=4, sort_keys=True))
settings = loads(SETTINGS_PATH.read_text())


def save_settings():
    """
    Save the settings.
    """
    logger.debug(f"Saving settings to {SETTINGS_PATH}")
    SETTINGS_PATH.write_text(dumps(settings, indent=4, sort_keys=True))


gui = CircuitPythonBundleManagerGUI(settings, SETTINGS_PATH, save_settings)
gui.lift()
logger.debug("Starting event loop")
gui.mainloop()
