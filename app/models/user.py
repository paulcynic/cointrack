from sqlalchemy import Integer, String, Column, Boolean
from sqlalchemy.orm import relationship
from . import Base


class User(Base):
    id = Column(Integer, primary_key=True, index=True, unique=True)
    name = Column(String(128), unique=True, nullable=False)
    password = Column(String(256), nullable=True)
    balance = Column(Integer, nullable=True)
    is_superuser = Column(Boolean, default=False)
    coins = relationship(
            "CoinPrice",
            cascade="all,delete-orphan",
            back_populates="submitter",
            uselist=True,
            )

