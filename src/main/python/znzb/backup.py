"""
Creates a backup of the Zanzibar SQLite database
"""
import datetime
import logging.handlers
import os
import sqlite3

from znzb import __version__
from znzb.common import init_logging
from znzb.config import config
from znzb.models import db_filename

logger = logging.getLogger(__name__)


def progress(status, remaining, total):
    logger.info(f'Copied {total - remaining} of {total} pages... - {status}')


def backup():
    logger.info(f'backup() - Start ({__version__})')
    logger.info(f'PID: {os.getpid()}')

    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    backup_filename = os.path.join(config.db_dir, f'zanzibar-{yesterday:%Y%m%d}.db')

    logger.info(f'Backup source: {db_filename}')
    logger.info(f'Backup destination: {backup_filename}')

    src = sqlite3.connect(db_filename)
    dst = sqlite3.connect(backup_filename)

    with dst:
        src.backup(dst, pages=10, progress=progress)

    dst.close()
    src.close()

    logger.info(f'backup() - Finish, PID: {os.getpid()}')


if __name__ == '__main__':
    init_logging('listener-backup.log')

    try:
        backup()
    except Exception as e:
        logger.fatal(e, exc_info=True)
