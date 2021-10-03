import logging
import os
import shutil
from contextlib import contextmanager

from sqlalchemy import Column, Integer, Float, String, create_engine, PrimaryKeyConstraint, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker

from znzb.common import init_logging
from znzb.config import config
from znzb.listener import __version__

logger = logging.getLogger(__name__)
db_filename = os.path.join(config.db_dir, 'zanzibar.db')
engine = create_engine(f'sqlite:///{db_filename}', connect_args={"check_same_thread": False}, echo=False)

Base = declarative_base()
Session = sessionmaker(bind=engine)


class Market(Base):
    __tablename__ = 'markets'

    id = Column(Integer, primary_key=True)
    market = Column(String, unique=True, nullable=False)
    status = Column(String, nullable=False)
    base = Column(String, nullable=False)
    quote = Column(String, nullable=False)
    pricePrecision = Column(Integer, nullable=False)
    minOrderInQuoteAsset = Column(Float, nullable=False)
    minOrderInBaseAsset = Column(Float, nullable=False)
    orderTypes = Column(String, nullable=False)


class Candle_1m(Base):
    __tablename__ = 'candles_1m'

    timestamp = Column(Integer, nullable=False)
    market_id = Column(Integer, ForeignKey(Market.id), nullable=False)
    open = Column(Float, nullable=False)
    high = Column(Float, nullable=False)
    low = Column(Float, nullable=False)
    close = Column(Float, nullable=False)
    volume = Column(Float, nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint(timestamp, market_id),
    )


class Candle_5m(Base):
    __tablename__ = 'candles_5m'

    timestamp = Column(Integer, nullable=False)
    market_id = Column(Integer, ForeignKey(Market.id), nullable=False)
    open = Column(Float, nullable=False)
    high = Column(Float, nullable=False)
    low = Column(Float, nullable=False)
    close = Column(Float, nullable=False)
    volume = Column(Float, nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint(timestamp, market_id),
    )


class Candle_1h(Base):
    __tablename__ = 'candles_1h'

    timestamp = Column(Integer, nullable=False)
    market_id = Column(Integer, ForeignKey(Market.id), nullable=False)
    open = Column(Float, nullable=False)
    high = Column(Float, nullable=False)
    low = Column(Float, nullable=False)
    close = Column(Float, nullable=False)
    volume = Column(Float, nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint(timestamp, market_id),
    )


class Candle_1d(Base):
    __tablename__ = 'candles_1d'

    timestamp = Column(Integer, nullable=False)
    market_id = Column(Integer, ForeignKey(Market.id), nullable=False)
    open = Column(Float, nullable=False)
    high = Column(Float, nullable=False)
    low = Column(Float, nullable=False)
    close = Column(Float, nullable=False)
    volume = Column(Float, nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint(timestamp, market_id),
    )


class HistoricalUpdate(Base):
    __tablename__ = 'historical_updates'

    market_id = Column(Integer, ForeignKey(Market.id), nullable=False)
    type = Column(String, nullable=False)
    status = Column(String, nullable=False)
    started = Column(Integer)
    ended = Column(Integer)
    updated = Column(Integer)

    __table_args__ = (
        PrimaryKeyConstraint(market_id, type),
    )



class Historical_1m(Base):
    __tablename__ = 'historical_1m'

    timestamp = Column(Integer, nullable=False)
    market_id = Column(Integer, ForeignKey(Market.id), nullable=False)
    open = Column(Float, nullable=False)
    high = Column(Float, nullable=False)
    low = Column(Float, nullable=False)
    close = Column(Float, nullable=False)
    volume = Column(Float, nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint(timestamp, market_id),
    )


@contextmanager
def session_scope():
    session = Session()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        logger.exception(e)
        raise
    finally:
        session.close()


def create_all():
    logger.info(f'create_all() - Start ({__version__})')
    logger.info(f'PID: {os.getpid()}')

    Base.metadata.create_all(engine)

    logger.info(f'create_all() - Finish')


def migrate():
    logger.info(f'migrate()- Start ({__version__})')
    logger.info(f'PID: {os.getpid()}')

    old_db_filename = os.path.join(config.db_dir, 'listener.db')
    new_db_filename = db_filename

    if not os.path.isfile(new_db_filename):
        logger.info(f'New DB does not exist: {new_db_filename}')

        if not os.path.isfile(old_db_filename):
            logger.fatal(f'Old DB does not exist: {old_db_filename}')
            raise FileNotFoundError(old_db_filename)

        shutil.copy(old_db_filename, new_db_filename)

        logger.info(f'Copied DB: {old_db_filename} to {new_db_filename}')

    # sanity check
    if os.path.isfile(new_db_filename):
        logger.info(f'DB does exist: {new_db_filename}')
        Base.metadata.create_all(engine)
    else:
        logger.fatal(f'DB does not exist: {new_db_filename}')
        raise FileNotFoundError(new_db_filename)

    logger.info(f'migrate() - Finish')


if __name__ == '__main__':
    init_logging('models.log')

    try:
        migrate()
        # create_all()
    except Exception as e:
        logger.fatal(e, exc_info=True)
