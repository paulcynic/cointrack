from pydantic import BaseModel
from typing import Optional


class RequestCoin(BaseModel):
    coin: Optional[str]
    currency: Optional[str]


class RequestFollowCoin(RequestCoin):
    lower: float
    upper: float
