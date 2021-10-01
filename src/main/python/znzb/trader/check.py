import datetime
import logging
import os
import zoneinfo

from python_bitvavo_api.bitvavo import Bitvavo

from znzb.trader import __version__
from znzb.common import init_logging
from znzb.config import config

logger = logging.getLogger(__name__)


def connect() -> Bitvavo:
    logger.debug('connect() - Start')

    logger.debug('connecting')
    bitvavo = Bitvavo({
        'APIKEY': config.bitvavo_api_key,
        'APISECRET': config.bitvavo_api_secret,
        'RESTURL': 'https://api.bitvavo.com/v2',
        'WSURL': 'wss://ws.bitvavo.com/v2/',
        'ACCESSWINDOW': 10000,
        'DEBUGGING': False,
    })

    logger.debug('connect() - Finish')
    return bitvavo


def get_assets(bitvavo):
    logger.debug('get_assets() - Start')

    response = bitvavo.assets({})
    for asset in response:
        print(asset)
        # print(f"Symbol: {row['symbol']}, Available: {row['available']}, In Order: {row['inOrder']}")

    logger.debug('get_assets() - Finish')


def get_time(bitvavo: Bitvavo) -> datetime:
    logger.debug('get_time() - Start')

    response = bitvavo.time()
    time = response['time']
    timezone = zoneinfo.ZoneInfo('Europe/Amsterdam')
    dt = datetime.datetime.fromtimestamp(time / 1000, timezone)

    logger.debug('get_time() - Finish')
    return dt


def get_balance(bitvavo):
    logger.debug('get_balance() - Start')

    response = bitvavo.balance({})
    for row in response:
        print(f"Symbol: {row['symbol']}, Available: {row['available']}, In Order: {row['inOrder']}")

    logger.debug('get_balance() - Finish')


def get_eur(bitvavo: Bitvavo) -> float:
    logger.debug('get_eur() - Start')

    response = bitvavo.balance({'symbol': 'EUR'})
    amount = float(response[0]['available'])

    logger.debug('get_eur() - Finish')
    return amount


def get_price_btc(bitvavo: Bitvavo) -> float:
    logger.debug('get_eur() - Start')

    response = bitvavo.tickerPrice({'market': 'BTC-EUR'})
    price = float(response['price'])

    logger.debug('get_btc_eur() - Finish')
    return price


def get_btc(bitvavo: Bitvavo) -> float:
    logger.debug('get_btc() - Start')

    response = bitvavo.balance({'symbol': 'BTC'})
    amount = float(response[0]['available'])

    logger.debug('get_btc() - Finish')
    return amount


def check():
    logger.info(f'check() - Start ({__version__})')
    logger.info(f'PID: {os.getpid()}')

    bitvavo = connect()
    time = get_time(bitvavo)
    get_assets(bitvavo)
    get_balance(bitvavo)
    eur = get_eur(bitvavo)
    btc = get_btc(bitvavo)
    price_btc = get_price_btc(bitvavo)

    logger.info(f'Bitvavo Time: {time:%Y-%m-%d %H:%M:%S}')
    logger.info(f'Balance EUR: € {eur:.02f}')
    logger.info(f'Balance BTC: € {btc * price_btc:.02f} = ₿ {btc:.09f} * {price_btc:.02f}')
    logger.info(f'Total: € {eur + btc * price_btc:.02f}')

    logger.info(f'check() - Finish')


if __name__ == '__main__':
    init_logging('trader-check.log')

    try:
        check()
    except Exception as e:
        logger.fatal(e, exc_info=True)
