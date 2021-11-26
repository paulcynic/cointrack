from .base import CRUDBase
from app.models.currency import Currency
from app.schemas.currency import CurrencyCreate, CurrencyUpdate


class CRUDCurrency(CRUDBase[Currency, CurrencyCreate, CurrencyUpdate]):
    ...


currency = CRUDCurrency(Currency)

