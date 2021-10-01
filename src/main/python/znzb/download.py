"""
Download Zanzibar SQLite database.
"""
import datetime
import fnmatch
import logging.handlers
import os

import paramiko

from znzb import __version__
from znzb.common import init_logging
from znzb.config import config

logger = logging.getLogger(__name__)


def download(hostname):
    logger.info(f'download({hostname})- Start ({__version__})')
    logger.info(f'PID: {os.getpid()}')

    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    backup_filename = f'listener-{yesterday:%Y%m%d}.db'
    local_filename = os.path.join(config.db_dir, backup_filename)

    if os.path.isfile(local_filename):
        logger.warning(f'Download exist: {local_filename}')

    conf = paramiko.SSHConfig()
    conf.parse(open(os.path.expanduser('~/.ssh/config')))
    host = conf.lookup(hostname)

    with paramiko.SSHClient() as ssh:
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.load_system_host_keys()

        logger.debug(f'Connecting: {hostname}')
        ssh.connect(host['hostname'], username=host['user'], port=host['port'])
        logger.debug(f'Connected: {hostname}')

        sftp = ssh.open_sftp()
        sftp.chdir('var/zanzibar/db')
        for file in sftp.listdir():
            if fnmatch.fnmatch(file, 'zanzibar-????????.db'):
                logger.debug(f'backup file: {file}')
                if file == backup_filename:
                    sftp.get(file, local_filename)

    if os.path.isfile(local_filename):
        logger.info(f'Downloaded: {local_filename}')
    else:
        logger.error(f'Not downloaded: {local_filename}')

    logger.info(f'download({hostname}) - Finish')


if __name__ == '__main__':
    init_logging('listener-download.log')

    # Reduce Paramiko logging
    transport = logging.getLogger('paramiko.transport')
    transport.setLevel(logging.WARNING)

    try:
        download(config.sftp_hostname)
    except Exception as e:
        logger.fatal(e, exc_info=True)
