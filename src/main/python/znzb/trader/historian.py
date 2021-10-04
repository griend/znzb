import datetime
import logging
import os
import time

from python_bitvavo_api.bitvavo import Bitvavo

from znzb.trader import __version__
from znzb.common import init_logging
from znzb.config import config
from znzb.models import session_scope, Market, HistoricalUpdate, Historical_1m

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


def populate_markets():
    logger.debug(f'populate_markets() - Start')

    connection = connect()
    response = connection.markets({})
    if 'error' in response:
        raise Exception(response)

    with session_scope() as session:
        for market in response:
            old = session.query(Market).filter_by(market=market['market']).first()
            if old:
                # logger.info(f'Update market: {market["market"]}')
                tmp = old
            else:
                tmp = Market()
                session.add(tmp)
                # logger.info(f'Insert market: {market["market"]}')
            tmp.market = market['market']
            tmp.status = market['status']
            tmp.base = market['base']
            tmp.quote = market['quote']
            tmp.pricePrecision = int(market['pricePrecision'])
            tmp.minOrderInQuoteAsset = float(market['minOrderInQuoteAsset'])
            tmp.minOrderInBaseAsset = float(market['minOrderInBaseAsset'])
            tmp.orderTypes = ', '.join(market['orderTypes'])

    logger.debug(f'populate_markets() - Finish')



def populate_historical_updates():
    logger.debug(f'populate_historical_updates() - Start ({__version__})')

    start_epoch = int(datetime.datetime(2020, 1, 1, 0, 0, 0).timestamp())
    end_epoch = int(datetime.datetime(2099, 12, 31, 23, 59, 59).timestamp())

    with session_scope() as session:
        for market in session.query(Market).filter(Market.status == 'trading').all():
            market_id = market.id
            type = '1m'
            old = session.query(HistoricalUpdate).filter(HistoricalUpdate.market_id == market_id).filter(HistoricalUpdate.type == type).first()
            if old:
                pass
            else:
                tmp = HistoricalUpdate()
                tmp.market_id = market.id
                tmp.type = type
                tmp.status = 'active'
                tmp.started = start_epoch
                tmp.ended = end_epoch
                tmp.updated = start_epoch
                session.add(tmp)

    logger.debug(f'populate_historical_updates() - Finish')


def populate_historical_1m():
    logger.debug(f'populate_historical_1m2() - Start ({__version__})')

    now_epoch = int(datetime.datetime.now().timestamp())
    connection = connect()

    with session_scope() as session:
        for update in session.query(HistoricalUpdate) \
                .filter(HistoricalUpdate.status == 'active') \
                .filter(HistoricalUpdate.type == '1m') \
                .filter(HistoricalUpdate.started <= now_epoch) \
                .filter(HistoricalUpdate.ended >= now_epoch) \
                .all():
            start_epoch = update.updated
            if start_epoch > now_epoch:
                start_epoch = now_epoch
            end_epoch = start_epoch + 60 * 60 * 12
            if end_epoch > now_epoch:
                end_epoch = now_epoch
            start_ms = start_epoch * 1000
            end_ms = end_epoch * 1000
            market = session.query(Market).filter(Market.id == update.market_id).one().market
            # start_dt = datetime.datetime.fromtimestamp(start_epoch)
            # print(f'{market=} {start_dt=}')

            response = connection.candles(market, '1m', {'start': start_ms, 'end': end_ms})
            if 'error' in response:
                raise Exception(response)

            reverse = response[::-1]
            for candle in reverse:
                timestamp = int(candle[0] / 1000)
                old = session.query(Historical_1m) \
                    .filter(Historical_1m.timestamp == timestamp) \
                    .filter(Historical_1m.market_id == update.market_id) \
                    .first()
                if old:
                    # print(f'Updating: {timestamp} {update.market_id}')
                    tmp = old
                else:
                    # print(f'Inserting: {timestamp} {update.market_id}')
                    tmp = Historical_1m()
                    session.add(tmp)
                tmp.timestamp = timestamp
                tmp.market_id = update.market_id
                tmp.open = float(candle[1])
                tmp.high = float(candle[2])
                tmp.low = float(candle[3])
                tmp.close = float(candle[4])
                tmp.volume = float(candle[5])
            update.updated = end_epoch
            end_dt = datetime.datetime.fromtimestamp(end_epoch)
            # print(f'{market=} {end_dt=}')
            logger.info(f'{market} ({update.market_id}) {end_dt:%Y-%m-%d %H:%M:%S}')

    logger.debug(f'populate_historical_1m2() - Finish')


def historian():
    logger.info(f'historian() - Start ({__version__})')
    logger.info(f'PID: {os.getpid()}')

    populate_markets()
    populate_historical_updates()

    for n in range(365 * 2):
        populate_historical_1m()
        time.sleep(60)

    logger.info(f'historian() - Finish')


if __name__ == '__main__':
    init_logging('trader-historian.log')

    try:
        historian()
    except Exception as e:
        logger.fatal(e, exc_info=True)
