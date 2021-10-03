import datetime
import logging
import os
import sqlite3
import sys

import numpy
import talib

from znzb.trader import __version__
from znzb.common import init_logging
from znzb.config import config

logger = logging.getLogger(__name__)

bank = 100.0
coin = 0.0
expense = 0.0
old_price = 0.0


def analyse(connection, market, dt):
    logger.debug(f'analyse({market}, {dt})')

    ts = int(dt.timestamp())
    closes = []

    cursor = connection.cursor()
    cursor.execute('''
      SELECT c.close
        FROM candles_1m c
        JOIN markets m
          ON m.id = c.market_id
       WHERE c.timestamp <=:ts
         AND m.market = :id
    ORDER BY timestamp DESC
       LIMIT 15 
    ''', (
        ts,
        market
    ))

    for row in cursor.fetchall():
        closes.append(row['close'])

    cursor.close()

    data = numpy.array(closes[::-1])
    rsi = talib.RSI(data)[-1]

    logger.debug(f'analyse({market}, {dt}) - Finish')
    return rsi, closes[1]


def buy(price):
    global bank
    global coin
    global expense

    expense += bank * 0.0025
    bank -= bank * 0.0025
    coin = bank / price
    bank = 0

    return True


def sell(price):
    global bank
    global coin
    global expense

    bank = coin * price
    expense += bank * 0.0025
    bank -= bank * 0.0025
    coin = 0

    return False


def simulate(market):
    logger.info(f'simulate({market}) - Start ({__version__})')
    logger.info(f'PID: {os.getpid()}')

    yesterday = datetime.date.today() - datetime.timedelta(1)
    start_dt = datetime.datetime(2021, 9, 28, 20, 30, 0)
    end_dt = datetime.datetime(yesterday.year, yesterday.month, yesterday.day, 23, 59, 59)
    start_epoch = int(start_dt.timestamp())
    end_epoch = int(end_dt.timestamp())
    db_filename = os.path.join(config.db_dir, f'zanzibar-{yesterday:%Y%m%d}.db')
    connection = sqlite3.connect(db_filename)
    connection.row_factory = sqlite3.Row
    in_position = False
    buy_price = 0.0

    for t in range(start_epoch, end_epoch, 60):
        dt = datetime.datetime.fromtimestamp(t)
        rsi, price = analyse(connection, market, dt)

        if not in_position and rsi < 30:
            in_position = buy(price)
            buy_price = price
            logger.info(f'{dt} {rsi:.02f} -  Buy {price:.02f} - Bank: {bank:8.02f} / Coin: {coin}')
        elif in_position and rsi > 70:
            if price > buy_price * 1.0125:
                in_position = sell(price)
                logger.info(f'{dt} {rsi:.02f} - Sell {price:.02f} - Bank: {bank:8.02f} / Coin: {coin}')
        # else:
        #     logger.info(f'{dt} {rsi:.02f}')

    logger.info(f'Bank: {bank:.02f}, coin: {coin}, expense: {expense:.02f}')
    logger.info(f'Total: {bank + coin * price:.02f}')

    logger.info(f'simulate({market}) - Finish')


if __name__ == '__main__':
    init_logging('trader-simulator.log')

    try:
        if len(sys.argv) > 1:
            market = sys.argv[1]
            simulate(market)
        else:
            msg = f'ERROR: market is missing on the command line'
            print(msg)
            logger.error(msg)
    except Exception as e:
        logger.fatal(e, exc_info=True)
