from pydantic import BaseModel
from .form_decorator import as_form


@as_form
class ShowCoinForm(BaseModel):
    coin: str
    currency: str


@as_form
class FollowCoinForm(ShowCoinForm):
    lower: float
    upper: float

