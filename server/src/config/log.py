"""
Logging
"""
import logging
import logging.config

from . import LOGGING_FILE


def init():
    """
    Initialize logging.
    """
    logging.config.fileConfig(LOGGING_FILE)
