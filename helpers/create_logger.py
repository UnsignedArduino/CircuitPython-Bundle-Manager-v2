import logging


def create_logger(name: str, level: int = logging.DEBUG) -> logging.Logger:
    """
    A simple function to create a logger. You would typically put this right
    under all the other modules you imported.

    And then call `logger.debug()`, `logger.info()`, `logger.warning()`,
    `logger.error()`, `logger.critical()`, and
    `logger.exception` everywhere in that module.

    :param name: A string with the logger name.
    :param level: A integer with the logger level. Defaults to logging.DEBUG.
    :return: A logging.Logger which you can use as a regular logger.
    """
    logger = logging.getLogger(name=name)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level=level)
    console_formatter = logging.Formatter("%(asctime)s - %(name)s - "
                                          "%(levelname)s - %(message)s")
    console_handler.setFormatter(fmt=console_formatter)
    console_handler.setLevel(level=level)
    logger.propagate = False
    if console_handler not in logger.handlers:
        logger.addHandler(hdlr=console_handler)
    logger.setLevel(level=level)
    logger.debug(f"Created logger named {repr(name)} with level {repr(level)}")
    logger.debug(f"Handlers for {repr(name)}: {repr(logger.handlers)}")
    return logger
