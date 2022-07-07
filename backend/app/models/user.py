from sqlalchemy import Integer, String, Column, Boolean
from sqlalchemy.orm import relationship
from . import Base


class User(Base):
    id = Column(Integer, primary_key=True, index=True, unique=True)
    first_name = Column(String(256), nullable=True)
    surname = Column(String(256), nullable=True)
    email = Column(String, index=True, nullable=False)
    hashed_password = Column(String(128), nullable=False)
    is_superuser = Column(Boolean, default=False)
    coins = relationship(
        "CoinPrice",
        cascade="all,delete-orphan",
        back_populates="submitter",
        uselist=True,
    )
