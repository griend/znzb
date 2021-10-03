import datetime
import logging
import os
import sys

import matplotlib.pyplot as plt
import pandas as pd
import sqlalchemy as sql
import talib

from . import __version__
from ..common import init_logging
from ..config import config

logger = logging.getLogger(__name__)


def __query(type):
    return f'''
        SELECT datetime(c.timestamp, 'unixepoch', 'localtime') AS dt,
               c.close AS price
          FROM candles_{type} c
          JOIN markets m
            ON m.id = c.market_id
         WHERE c.timestamp >= :start
           AND m.market = :market
    '''

def __df(connection, market, type):
    start = int(datetime.datetime(2021, 9, 29, 0, 0, 0).timestamp())

    return pd.read_sql_query(__query(type),
                              connection,
                              params={'start': start, 'market': market},
                              index_col='dt',
                              parse_dates={'dt': '%Y-%m-%d %H:%M:%S'})

def analyse(filename, market):
    logger.debug(f'analyser({filename})- Start ({__version__})')

    connection = sql.create_engine(f'sqlite:///{filename}')

    # Fetch data from SQLite database
    df_1m = __df(connection, market, '1m')
    df_5m = __df(connection, market, '5m')
    df_1h = __df(connection, market, '1h')
    df_1d = __df(connection, market, '1d')

    df_rsi = talib.RSI(df_5m['price'])

    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()

    df_rsi.plot(ax=ax2, label='RSI', color='lightgray')

    ax2.set_ylim(0, 100)
    ax2.axhline(30, color='r', linestyle='--')
    ax2.axhline(70, color='r', linestyle='--')

    df_1d['price'].plot(ax=ax1, label='1 day')
    df_1h['price'].plot(ax=ax1, label='1 hour')
    df_5m['price'].plot(ax=ax1, label='5 min')
    df_1m['price'].plot(ax=ax1, label='1 min')

    ax1.set_ylabel('Price (€)')
    ax1.legend()

    ax2.set_ylabel('RSI')

    plt.title(market)
    plt.grid()
    plt.xlabel('Date / Time')

    plt.show()

    logger.debug(f'analyser({filename}) - Finish')


def main(market):
    logger.info(f'main()- Start ({__version__})')
    logger.info(f'PID: {os.getpid()}')

    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    db_filename = os.path.join(config.db_dir, f'zanzibar-{yesterday:%Y%m%d}.db')

    if not os.path.isfile(db_filename):
        logger.error(f'Datebase does not exist: {db_filename}')
    else:
        analyse(db_filename, market)

    logger.info(f'main() - Finish')


if __name__ == '__main__':
    init_logging('analyser.log')

    try:
        if len(sys.argv) > 1:
            market = sys.argv[1]
        else:
            market = 'BTC-EUR'
        main(market)
    except Exception as e:
        logger.fatal(e, exc_info=True)
