import logging

from TkZero.MainWindow import MainWindow

from circuitpython_bundle_manager import CircuitPythonBundleManager
from helpers.create_logger import create_logger

logger = create_logger(name=__name__, level=logging.DEBUG)


class CircuitPythonBundleManagerGUI(MainWindow):
    """
    The GUI for the CircuitPython Bundle Manager v2.
    """
    def __init__(self):
        self.cpybm = CircuitPythonBundleManager()
        logger.debug("Creating GUI")
        super().__init__()
        self.title = "CircuitPython Bundle Manager v2"
