from .base import CRUDBase
from app.models.coin import Coin
from app.schemas.coin import CoinCreate, CoinUpdate


class CRUDCoin(CRUDBase[Coin, CoinCreate, CoinUpdate]):
    ...


coin = CRUDCoin(Coin)

