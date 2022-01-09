import asyncio
import httpx
from httpx import HTTPError
from fastapi import APIRouter, Form, Query, Depends

from sqlalchemy.orm import Session
from pydantic import HttpUrl
from typing import Optional, List

from app import crud
from app.core.scheduler import scheduler
from app.api import deps
from app.clients.gecko_client import GeckoClient
from app.schemas.coin_price import CoinPriceCreate
from app.services import generate_follow_list, validate_phone

URL = 'https://api.coingecko.com/api/v3/simple/price'


router = APIRouter()


#def get_simple_price(
#        url: HttpUrl,
#        coin: str,
#        currency: str,
#        limit: float,
#        db: Session
#        ) -> dict:
#    params = {'ids': coin, 'vs_currencies': currency}
#    headers={"User-agent": "cointrack bot 0.1"}
#    try:
#        raw_response = httpx.get(url, params=params, headers=headers)
#        raw_response.raise_for_status()
#    except HTTPError:
#        raise Exception(
#                    f"Request failure:\n"
#                    f"GET: {url}\n"
#                )
#
#    response = raw_response.json()
#    name = [key for key in response][0]
#    label = [key for key in response[name]][0]
#    price = float(response[name][label])
#    coin_price_in = CoinPriceCreate(
#            coin_name = name,
#            currency_label = label,
#            price = price,
#            submitter_id = 1)
#    crud.coin_price.create(db=db, obj_in=coin_price_in)
#    if price > limit:
#        tele_name = str(name).replace('-', '\\-')
#        tele_price = str(price).replace('.', '\\.')
#        send_message(f'{tele_name} {tele_price} {label}')
#    return response


@router.post("/request/coin/", status_code=201)
def post_request_coin(
        gecko_client: GeckoClient = Depends(GeckoClient),
        coin: str = Form(...),
        currency: str = Form(...),
        ):
    task_id = f'{coin}_{currency}'
    scheduler.add_job(gecko_client.send_telegram_message, "interval", [coin, currency], id=task_id, replace_existing=True, seconds=20)
    jobs = scheduler.get_jobs()
    for job in jobs:
        print(job.id)
    params={"ids": coin, "vs_currencies": currency}
    response = gecko_client.get_simple_price(params=params)
    return response


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
            coin_name = name,
            currency_label = label,
            price = price,
            submitter_id = 1)
    coin_list.append(coin_price_in)


@router.get("/follow_all/", status_code=200)
async def follow_all_coins(*,
        url: HttpUrl = URL,
        db: Session = Depends(deps.get_db)
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
        headers={"User-agent": "cointrack bot 0.2"}
        task = asyncio.create_task(get_simple_price_async(coin_list, url, params, headers))
        tasks.append(task)
    await asyncio.gather(*tasks)
    return coin_list


@router.get("/unify_phone_from_query/")
def phone_from_query(*, phone: Optional[str] = Query(None, example="89991234567")):
    resp_phone = validate_phone(phone)
    return {"phone": resp_phone}

