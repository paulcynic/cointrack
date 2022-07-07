import asyncio
import httpx
from httpx import HTTPError
from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session
from pydantic import HttpUrl
from typing import Any, List

from app import crud
from app.core.scheduler import scheduler
from app.api import deps
from app.clients.gecko_client import GeckoClient
from app.schemas.coin_price import CoinPriceCreate
from app.schemas.body import RequestCoin, RequestFollowCoin

from app.services import generate_follow_list
from app.core.config import settings

from app.models.user import User

router = APIRouter()


@router.get("/my-coins/", status_code=200)
def fetch_user_coins(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Fetch all coin request of current user
    """
    coins = current_user.coins[:-20:-1]
    if not coins:
        return list()

    return list(coins)


@router.post("/", status_code=200)
def show_price(
        *, request_coin: RequestCoin,
        gecko_client: GeckoClient = Depends(deps.get_gecko_client),
) -> dict:
    params = {"ids": request_coin.coin,
              "vs_currencies": request_coin.currency}
    simple_price = gecko_client.get_simple_price(params=params)
    return simple_price
    # Response example:{ "bitcoin": { "usd": 19075.48 }}


@router.post("/follow/", status_code=201)
def follow_coin(
        *, request_coin: RequestFollowCoin,
        gecko_client: GeckoClient = Depends(deps.get_gecko_client),
        current_user: User = Depends(deps.get_current_user),
):
    try:
        assert request_coin.lower < request_coin.upper
    except AssertionError:
        raise HTTPException(status_code=422,
                            detail="Lower limit should be less than Upper limit!")
    task_id = f'{request_coin.coin}_{request_coin.currency}'
    scheduler.add_job(
        gecko_client.send_telegram_message,
        "interval",
        [request_coin.coin, request_coin.currency,
            request_coin.lower, request_coin.upper, current_user.id],
        id=task_id,
        replace_existing=True,
        seconds=15,
    )
    return {"detail": f"Your {request_coin.coin} {request_coin.currency} is tracked!"}


async def get_simple_price_async(coin_list: List, url: HttpUrl, params: dict, headers: dict):
    try:
        async with httpx.AsyncClient() as client:
            raw_response = await client.get(url=url, params=params, headers=headers)
        raw_response.raise_for_status()
    except HTTPError:
        raise Exception(
            f"AsyncRequest failure:\n"
            f"GET: {url}\n"
        )
    response = raw_response.json()
    name = [key for key in response][0]
    label = [key for key in response[name]][0]
    price = float(response[name][label])
    coin_price_in = CoinPriceCreate(
        coin_name=name,
        currency_label=label,
        price=price,
        submitter_id=1)
    coin_list.append(coin_price_in)


@router.get("/all/", status_code=200)
async def show_all_coins(*,
                         url: HttpUrl = settings.URL_SIMPLE_PRICE,
                         db: Session = Depends(deps.get_db),
                         ):
    coins = crud.coin.get_multi(db=db, limit=4)
    coin_names = [coin.name for coin in coins]
    currencies = crud.currency.get_multi(db=db, limit=5)
    currency_labels = [currency.label for currency in currencies]
    tasks = []
    coin_list = []
    for coin_currency in generate_follow_list(coin_names, currency_labels):
        coin, currency = coin_currency
        params = {'ids': coin, 'vs_currencies': currency}
        headers = {"User-agent": "cointrack bot 0.2"}
        task = asyncio.create_task(
            get_simple_price_async(coin_list, url, params, headers))
        tasks.append(task)
    await asyncio.gather(*tasks)
    return coin_list
