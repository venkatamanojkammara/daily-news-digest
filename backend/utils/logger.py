"""
Docstring for backend.utils.logger

Central logging comnfiguration for entire project.
All modules should use this instead of print().

"""


#---------------------------------------------------------
# Imports
#---------------------------------------------------------
import logging
import os
from logging.handlers import RotatingFileHandler

from backend.config import LOG_LEVEL, LOG_DIR


#---------------------------------------------------------
# lOGGER setup
#---------------------------------------------------------
def get_logger(name: str) -> logging.Logger:
    """
    Create and return a configured logger.

    Logs to:
    - console
    - Rotating files in LOG_DIR
    """

    logger = logging.getLogger(name)

    if logger.handlers:
        return logger
    
    logger.setLevel(LOG_LEVEL.upper())
    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")

    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    log_file = os.path.join(LOG_DIR, "app.log")
    fh = RotatingFileHandler(log_file, maxBytes=2_000_000, backupCount=3)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    return logger
