import logging
import os
from contextlib import contextmanager

from sqlalchemy import Column, Integer, Float, String, create_engine, PrimaryKeyConstraint, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker

from ..config import config
from ..common import init_logging


logger = logging.getLogger(__name__)
db_filename = os.path.join(config.db_dir, 'listener.db')
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
    logger.info(f'create_all() - Start, PID: {os.getpid()}')

    Base.metadata.create_all(engine)

    logger.info(f'create_all() - Finish, PID: {os.getpid()}')


if __name__ == '__main__':
    init_logging('listener-models.log')

    try:
        create_all()
    except Exception as e:
        logger.fatal(e, exc_info=True)
