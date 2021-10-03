import logging
import logging.handlers
import os
import sys

from znzb.config import config


def init_logging(log_filename: str = None):
    format = logging.Formatter('%(asctime)s %(name)s %(levelname)s - %(message)s')
    if log_filename:
        filename = os.path.join(config.log_dir, log_filename)
        fh = logging.handlers.TimedRotatingFileHandler(filename=filename, when="midnight", backupCount=30)
        fh.setFormatter(format)
        fh.setLevel(logging.DEBUG)

    console = logging.StreamHandler()
    console.setFormatter(format)

    if sys.stdout.isatty():
        console.setLevel(logging.INFO)
    else:
        console.setLevel(logging.FATAL)

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    if log_filename:
        logger.addHandler(fh)

    logger.addHandler(console)
