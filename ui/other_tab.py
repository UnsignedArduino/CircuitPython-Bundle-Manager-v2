import logging

from TkZero.Notebook import Tab, Notebook

from circuitpython_bundle_manager import CircuitPythonBundleManager
from helpers.create_logger import create_logger

logger = create_logger(name=__name__, level=logging.DEBUG)


class OtherTab(Tab):
    """
    The OtherTab.
    """
    def __init__(self, parent: Notebook, cpybm: CircuitPythonBundleManager):
        """
        Make a OtherTab.

        :param parent: The parent of the tab. Should be a
         TkZero.Notebook.Notebook.
        :param cpybm: The CircuitPythonBundleManager instance.
        """
        super().__init__(parent, "Other")
        self.cpybm = cpybm
        logger.debug("Making other tab")
