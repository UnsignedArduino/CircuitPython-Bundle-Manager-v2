import logging
from helpers.create_logger import create_logger
from gui import CircuitPythonBundleManagerGUI

logger = create_logger(name=__name__, level=logging.DEBUG)

gui = CircuitPythonBundleManagerGUI()

logger.debug("Starting event loop")
gui.mainloop()
