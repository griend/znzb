import datetime
import logging
import logging.handlers
import os
import signal
import sys
import time

from python_bitvavo_api.bitvavo import Bitvavo
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .models import Market, Candle_1m, Candle_5m, Candle_1h, Candle_1d
from ..config import Config

logger = logging.getLogger(__name__)
config = Config()
db_filename = os.path.join(config.db_dir, 'listener.db')

running = True
market_id_cache = {}


def init_logging(log_filename: str = 'listener.log') -> None:
    """
    Configure the logging.

    :param log_filename:
    """
    format = logging.Formatter('%(asctime)s %(name)s %(levelname)s - %(message)s')
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

    logger.addHandler(fh)
    logger.addHandler(console)


def signal_handler(signal, *args):
    """

    :param signal:
    :param args:
    :return:
    """
    global running
    running = False
    logger.info(f'Caught signal: {signal}')


def error_callback(error):
    try:
        logger.error(error)
    except Exception as e:
        logger.error(e, exc_info=True)


def time_callback(response):
    try:
        time = int(response['time'])
        dt = datetime.datetime.fromtimestamp(time / 1000)
        logger.info(f'Bitvavo time: {dt:%Y-%m-%d %H:%M:%S}')
    except Exception as e:
        logger.error(e, exc_info=True)


def markets_callback(response):
    try:
        engine = create_engine(f'sqlite:///{db_filename}')
        Session = sessionmaker(bind=engine)
        session = Session()
        for market in response:
            old = session.query(Market).filter_by(market=market['market'])

            if old:
                tmp = old
            else:
                tmp = Market()
                session.add(tmp)

            tmp.market = market['market']
            tmp.status = market['status']
            tmp.base = market['base']
            tmp.quote = market['quote']
            tmp.pricePrecision = int(market['pricePrecision'])
            tmp.minOrderInQuoteAsset = float(market['minOrderInQuoteAsset'])
            tmp.minOrderInBaseAsset = float(market['minOrderInBaseAsset'])
            tmp.orderTypes = ', '.join(market['orderTypes'])

        session.commit()
    except Exception as e:
        logger.error(e, exc_info=True)


def populate_market_id_cache():
    try:
        engine = create_engine(f'sqlite:///{db_filename}')
        Session = sessionmaker(bind=engine)
        session = Session()

        for market in session.query(Market).filter_by(status='trading'):
            market_id_cache[market.market] = market.id
        session.commit()
    except Exception as e:
        logger.error(e, exc_info=True)


def candle_1m_callback(response):
    try:
        engine = create_engine(f'sqlite:///{db_filename}')
        Session = sessionmaker(bind=engine)
        session = Session()
        timestamp = int(response['candle'][0][0] / 1000)
        market_id = market_id_cache[response['market']]
        old = session.query(Candle_1m).filter_by(timestamp=timestamp, market_id=market_id)

        if old:
            tmp = old
        else:
            tmp = Candle_1m()
            session.add(tmp)

        tmp.open = float(response['candle'][0][1])
        tmp.high = float(response['candle'][0][2])
        tmp.low = float(response['candle'][0][3])
        tmp.close = float(response['candle'][0][4])
        tmp.volume = float(response['candle'][0][5])
        session.commit()
        logger.info(f'1m {timestamp} {market_id} {tmp.open} {tmp.high} {tmp.low} {tmp.close} {tmp.volume}')
    except Exception as e:
        logger.error(e, exc_info=True)


def candle_5m_callback(response):
    try:
        engine = create_engine(f'sqlite:///{db_filename}')
        Session = sessionmaker(bind=engine)
        session = Session()
        timestamp = int(response['candle'][0][0] / 1000)
        market_id = market_id_cache[response['market']]
        old = session.query(Candle_5m).filter_by(timestamp=timestamp, market_id=market_id)

        if old:
            tmp = old
        else:
            tmp = Candle_5m()
            session.add(tmp)

        tmp.open = float(response['candle'][0][1])
        tmp.high = float(response['candle'][0][2])
        tmp.low = float(response['candle'][0][3])
        tmp.close = float(response['candle'][0][4])
        tmp.volume = float(response['candle'][0][5])
        session.commit()
        logger.info(f'5m {timestamp} {market_id} {tmp.open} {tmp.high} {tmp.low} {tmp.close} {tmp.volume}')
    except Exception as e:
        logger.error(e, exc_info=True)


def candle_1h_callback(response):
    try:
        engine = create_engine(f'sqlite:///{db_filename}')
        Session = sessionmaker(bind=engine)
        session = Session()
        timestamp = int(response['candle'][0][0] / 1000)
        market_id = market_id_cache[response['market']]
        old = session.query(Candle_1h).filter_by(timestamp=timestamp, market_id=market_id)

        if old:
            tmp = old
        else:
            tmp = Candle_1h()
            session.add(tmp)

        tmp.open = float(response['candle'][0][1])
        tmp.high = float(response['candle'][0][2])
        tmp.low = float(response['candle'][0][3])
        tmp.close = float(response['candle'][0][4])
        tmp.volume = float(response['candle'][0][5])
        session.commit()
        logger.info(f'1h {timestamp} {market_id} {tmp.open} {tmp.high} {tmp.low} {tmp.close} {tmp.volume}')
    except Exception as e:
        logger.error(e, exc_info=True)


def candle_1d_callback(response):
    try:
        engine = create_engine(f'sqlite:///{db_filename}')
        Session = sessionmaker(bind=engine)
        session = Session()
        timestamp = int(response['candle'][0][0] / 1000)
        market_id = market_id_cache[response['market']]
        old = session.query(Candle_1d).filter_by(timestamp=timestamp, market_id=market_id)

        if old:
            tmp = old
        else:
            tmp = Candle_1d()
            session.add(tmp)

        tmp.open = float(response['candle'][0][1])
        tmp.high = float(response['candle'][0][2])
        tmp.low = float(response['candle'][0][3])
        tmp.close = float(response['candle'][0][4])
        tmp.volume = float(response['candle'][0][5])
        session.commit()
        logger.info(f'1d {timestamp} {market_id} {tmp.open} {tmp.high} {tmp.low} {tmp.close} {tmp.volume}')
    except Exception as e:
        logger.error(e, exc_info=True)


def main():
    logger.info(f'main() - Start, PID: {os.getpid()}')
    signal.signal(signal.SIGTERM, signal_handler)

    bitvavo = Bitvavo()

    websocket = bitvavo.newWebsocket()
    websocket.setErrorCallback(error_callback)
    websocket.time(time_callback)
    websocket.markets({}, markets_callback)

    populate_market_id_cache()

    markets = [
        'BTC-EUR',
        'ETH-EUR',
    ]

    for market in markets:
        websocket.subscriptionCandles(market, '1m', candle_1m_callback)
        websocket.subscriptionCandles(market, '5m', candle_5m_callback)
        websocket.subscriptionCandles(market, '1h', candle_1h_callback)
        websocket.subscriptionCandles(market, '1d', candle_1d_callback)

    try:
        limit = bitvavo.getRemainingLimit()

        while running and limit > 0:
            time.sleep(0.5)
            limit = bitvavo.getRemainingLimit()
    except KeyboardInterrupt:
        logger.info(f'Caught Ctrl-C')
    finally:
        websocket.closeSocket()

    logger.info(f'main() - Finish')


if __name__ == '__main__':
    try:
        init_logging()
        main()
    except Exception as e:
        logger.fatal(e, exc_info=True)
