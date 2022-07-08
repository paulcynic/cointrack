from pydantic import BaseModel
from typing import Optional


class CoinBase(BaseModel):
    name: Optional[str]


class CoinCreate(CoinBase):
    name: str


class CoinUpdate(CoinBase):
    name: str


# Properties shared by models stored in DB
class CoinInDBBase(CoinBase):
    id: int

    class Config:
        orm_mode = True
# Pydantic’s orm_mode (which you can see in CoinInDBBase) will tell the
# Pydantic model to read the data even if it is not a dict, but an ORM model.

# Properties to return to client
class Coin(CoinInDBBase):
    pass


# Properties properties stored in DB
class CoinInDB(CoinInDBBase):
    pass
