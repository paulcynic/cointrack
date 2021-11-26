from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from . import Base


class Currency(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128), nullable=True)
    label = Column(String(4), index=True, nullable=False)
    labels = relationship("CoinPrice",
            back_populates="submitter_label",
            cascade="all,delete-orphan",
            uselist=True
            )

