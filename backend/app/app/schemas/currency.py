from pydantic import BaseModel
from typing import Optional


class CurrencyBase(BaseModel):
    label: Optional[str]


class CurrencyCreate(CurrencyBase):
    label: str


class CurrencyUpdate(CurrencyBase):
    label: str


# Properties shared by models stored in DB
class CurrencyInDBBase(CurrencyBase):
    id: int

    class Config:
        orm_mode = True
# Pydantic’s orm_mode (which you can see in CurrencyInDBBase) will tell the
# Pydantic model to read the data even if it is not a dict, but an ORM model.

# Properties to return to client
class Currency(CurrencyInDBBase):
    pass


# Properties properties stored in DB
class CurrencyInDB(CurrencyInDBBase):
    pass

