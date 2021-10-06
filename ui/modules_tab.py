import logging
from TkZero.Notebook import Tab, Notebook


from helpers.create_logger import create_logger

logger = create_logger(name=__name__, level=logging.DEBUG)


class ModulesTab(Tab):
    """
    The ModulesTab.
    """
    def __init__(self, parent: Notebook):
        """
        Make a ModulesTab.

        :param parent: The parent of the tab. Should be a
         TkZero.Notebook.Notebook.
        """
        super().__init__(parent, "Modules")
        logger.debug("Making modules tab")
