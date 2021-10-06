import logging
from pathlib import Path

from gui import CircuitPythonBundleManagerGUI
from helpers.create_logger import create_logger

logger = create_logger(name=__name__, level=logging.DEBUG)

ICON_PATH = Path.cwd() / "icon.png"

gui = CircuitPythonBundleManagerGUI()

logger.debug("Starting event loop")
gui.mainloop()
