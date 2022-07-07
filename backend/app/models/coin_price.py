from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship

from . import Base


class CoinPrice(Base):
    id = Column(Integer, primary_key=True, index=True)
    coin_name = Column(String(128), ForeignKey("coin.name"), nullable=False)
    currency_label = Column(String(4), ForeignKey("currency.label"), nullable=False)
    price = Column(Float, nullable=True)
    current_datetime = Column(DateTime, default=datetime.utcnow, nullable=True)
    submitter_id = Column(Integer, ForeignKey("user.id"), index=True, nullable=False)
    submitter_label = relationship("Currency", back_populates="labels")
    submitter = relationship("User", back_populates="coins")
    submitter_coin = relationship("Coin", back_populates="coin_name")

