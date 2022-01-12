import typing as t
from sqlalchemy.orm import Session

from httpx import Client, Response, HTTPError

from app import crud
from app.api import deps
from app.core.config import settings
from app.schemas.coin_price import CoinPriceCreate


class GeckoClientError(Exception):
    def __init__(self, message: str, raw_response: t.Optional[Response] = None):
        self.message = message
        self.raw_response = raw_response
        super().__init__(self.message)


class GeckoClient:
    base_url: str = settings.URL_SIMPLE_PRICE
    base_error: t.Type[GeckoClientError] = GeckoClientError

    def __init__(self) -> None:
        self.session = Client()
        self.session.headers.update(
                {"Content-Type": "application/json",
                    "User-agent": "cointrack bot 0.1"})

    def _perform_request(self, method: str, url: str, *args, **kwargs) -> Response:
        res = None
        try:
            res = getattr(self.session, method)(url, *args, **kwargs)
            res.raise_for_status()
        except HTTPError:
            raise self.base_error(
                    f"{self.__class__.__name__} request failure:\n"
                    f"{method.upper()}:\n"
                    f"Message: {res is not None and res.text}",
                    raw_response=res,
                    )
        return res

    def get_simple_price(self, *args, **kwargs) -> dict:
        raw_response = self._perform_request("get", self.base_url, *args, **kwargs)
        response = raw_response.json()
        return response

    def _add_response_to_db(self, response: dict, db: Session) -> CoinPriceCreate:
        name = [key for key in response][0]
        label = [key for key in response[name]][0]
        price = float(response[name][label])
        coin_price_in = CoinPriceCreate(
                coin_name = name,
                currency_label = label,
                price = price,
                submitter_id = 1)
        crud.coin_price.create(db=db, obj_in=coin_price_in)
        return coin_price_in

    def _create_telegram_message(self, coin_price: CoinPriceCreate,) -> str:
        tele_name = str(coin_price.coin_name).replace('-', '\\-')
        tele_price = str(coin_price.price).replace('.', '\\.')
        tele_label = str(coin_price.currency_label).upper()
        return f'{tele_name} {tele_price} {tele_label}'

    def send_telegram_message(self, coin, currency, lower, upper) -> dict:
        get_params={"ids": coin, "vs_currencies": currency}
        res = self.get_simple_price(params=get_params)
        db = deps.SessionLocal()
        db_obj = self._add_response_to_db(res, db)
        db.close()
        if 0 < db_obj.price < lower or upper < db_obj.price:
            bot_message = self._create_telegram_message(db_obj)
        else:
            telecoin = coin.replace('-', '\\-')
            bot_message = f"Your {telecoin} {currency} is tracked"
        bot_token = settings.TELEGRAM_BOT_TOKEN
        bot_chatId = settings.BOT_CHAT_ID
        params = {'chat_id': bot_chatId, 'parse_mode': 'MarkdownV2', 'text': bot_message}
        response = self._perform_request('get', f'https://api.telegram.org/bot{bot_token}/sendMessage', params=params)
        return response.json()
