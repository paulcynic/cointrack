from .base import CRUDBase
from app.models.coin_price import CoinPrice
from app.schemas.coin_price import CoinPriceCreate


class CRUDCoinPrice(CRUDBase[CoinPrice, CoinPriceCreate, CoinPriceCreate]):
    ...


coin_price = CRUDCoinPrice(CoinPrice)

