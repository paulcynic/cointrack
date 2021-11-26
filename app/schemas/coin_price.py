from datetime import datetime
from pydantic import BaseModel
from typing import Sequence, Optional


class CoinPriceBase(BaseModel):
    currency_name: Optional[str]
    currency_label: Optional[str]
    price: Optional[float] = None
    current_datetime: Optional[datetime] = None
    submitter_id: Optional[int]


class CoinPriceCreate(CoinPriceBase):
    currency_name: str
    currency_label: str
    price: float
    current_datetime: datetime
    submitter_id: int


# Properties shared by models stored in DB
class CoinPriceInDBBase(CoinPriceBase):
    id: int

    class Config:
        orm_mode = True
# Pydantic’s orm_mode (which you can see in CoinPriceInDBBase) will tell the
# Pydantic model to read the data even if it is not a dict, but an ORM model.

# Properties to return to client
class CoinPrice(CoinPriceInDBBase):
    pass


# Properties properties stored in DB
class CoinPriceInDB(CoinPriceInDBBase):
    pass


class CoinPriceSearchResults(BaseModel):
    results: Sequence[CoinPrice]

