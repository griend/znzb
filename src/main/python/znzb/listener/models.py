import datetime
import os

from sqlalchemy import Column, Integer, Float, String, create_engine, PrimaryKeyConstraint, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker

from ..config import Config

Base = declarative_base()

config = Config()

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
    # created = Column(TIMESTAMP, default=datetime.datetime.utcnow, nullable=False)
    # updated = Column(TIMESTAMP, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow, nullable=False)


class Candle_1m(Base):
    __tablename__ = 'candles_1m'

    timestamp = Column(Integer, nullable=False)
    market_id = Column(Integer, ForeignKey(Market.id), nullable=False)
    open = Column(Float, nullable=False)
    high = Column(Float, nullable=False)
    low = Column(Float, nullable=False)
    close = Column(Float, nullable=False)
    volume = Column(Float, nullable=False)
    # created = Column(TIMESTAMP, default=datetime.datetime.utcnow, nullable=False)
    # updated = Column(TIMESTAMP, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow, nullable=False)

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


def get_engine():
    db_filename = os.path.join(config.db_dir, 'listener.db')
    engine = create_engine(f'sqlite:///{db_filename}')

    return engine


def get_Session():
    engine = get_engine()
    Session = sessionmaker(bind=engine)

    return Session


if __name__ == '__main__':
    engine = get_engine()

    Base.metadata.create_all(engine)
