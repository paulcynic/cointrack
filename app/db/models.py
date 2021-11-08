import datetime
from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy import Column, Integer, DateTime, Numeric, String, ForeignKey
from sqlalchemy.orm import relationship

#from base_class import Base

from sqlalchemy.ext.declarative import declarative_base

#engine = create_engine('postgresql://paulcynic@localhost/cointrack_db', echo=True)
Base = declarative_base()

class Coin(Base):
    __tablename__ = 'coin'
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(256), nullable=False)
    name = Column(String(256), nullable=False)
    coin_ref = relationship("CoinPriceTime", back_populates="coin")


class Currency(Base):
    __tablename__ = 'currency'
    id = Column(Integer, primary_key=True, index=True)
    label = Column(String(4), nullable=False, unique=True)
    currency_name = Column(String(256), nullable=True)
    currency_ref = relationship("CoinPriceTime", back_populates="currency")


class CoinPriceTime(Base):
    __tablename__ = 'coin_price_time'
    id = Column(Integer, primary_key=True, nullable=False)
    coin_id = Column(Integer, ForeignKey("coin.id"), nullable=False)
    currency_label = Column(String(4), ForeignKey("currency.label"), nullable=False)
    price = Column(Numeric(12,2), nullable=False)
    current_time = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    coin = relationship("Coin", back_populates="coin_ref")
    currency = relationship("Currency", back_populates="currency_ref")


#Base.metadata.create_all(engine)

