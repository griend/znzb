import datetime
import logging.handlers
import os
import sqlite3

from ..common import init_logging
from ..config import config

logger = logging.getLogger(__name__)
db_filename = os.path.join(config.db_dir, 'listener.db')


def progress(status, remaining, total):
    logger.info(f'Copied {total - remaining} of {total} pages... - {status}')


def backup():
    logger.info(f'backup() - Start, PID: {os.getpid()}')

    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    backup_filename = os.path.join(config.db_dir, f'listener-{yesterday:%Y%m%d}.db')

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
