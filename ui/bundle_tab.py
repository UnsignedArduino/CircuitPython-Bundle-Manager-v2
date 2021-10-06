import logging
from TkZero.Notebook import Tab, Notebook


from helpers.create_logger import create_logger

logger = create_logger(name=__name__, level=logging.DEBUG)


class BundleTab(Tab):
    """
    The BundleTab.
    """
    def __init__(self, parent: Notebook):
        """
        Make a BundleTab.

        :param parent: The parent of the tab. Should be a
         TkZero.Notebook.Notebook.
        """
        super().__init__(parent, "Bundle")
        logger.debug("Making bundle tab")
