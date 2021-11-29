from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from . import Base


class Coin(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128), unique=True, nullable=True)
    coin_name = relationship("CoinPrice",
            back_populates="submitter_coin",
            cascade="all,delete-orphan",
            uselist=True
            )
