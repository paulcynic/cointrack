import requests
import json
from fastapi import FastAPI, APIRouter, Cookie, Body, Form, Query, HTTPException, Request
from fastapi.responses import Response, RedirectResponse
# Из fastapi импортируем Jinja2Templates
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles


from typing import Optional, Any
# Из pathlib импортируем путь для папки с шаблонами 
from pathlib import Path

# Импортируем валидирующие функции, классы, базу с пользователями
from app.validators import get_username_from_signed_string, sign_data, verify_password, validate_phone, create_user_cookie
from app.schemas import User, UserEx
from app.user_data import USERS


app = FastAPI(title="DemoAuthCointrack", openapi_url="/rock/openapi.json")
router = APIRouter()

BASE_PATH = Path(__file__).resolve().parent
TEMPLATES = Jinja2Templates(directory=str(BASE_PATH/"templates"))
app.mount("/static", StaticFiles(directory=str(BASE_PATH/"static")), name="static")

# читает куку "username" как параметр функции
@router.get("/", status_code=200) #response_model=User
def index_page(request: Request, response: Response, username: Optional[str] = Cookie(default=None)):
    login_page = TEMPLATES.TemplateResponse("login.html", {"request": request},)
    if username is None:
        return login_page
    try:
        valid_username = get_username_from_signed_string(username)
    except ValueError:
        response = login_page
        response.delete_cookie("username")
        return response
    url = app.url_path_for("request_coin")
    response = RedirectResponse(url=url)
    return response
    #return USERS[valid_username]


#Response(f"Hello, {USERS[valid_username]['name']}!<br />Balance: {USERS[valid_username]['balance']}.", media_type="text/html")


# читает переданные данные формы "username", "password" как параметры функции
@router.post("/login/", status_code=201)
def process_login_page(*, request: Request, response: Response, username: str = Form(...), password: str = Form(...)):
    user = USERS.get(username)
    #Если не найдёт ключ, вернёт пустое значение
    #user = users[username] выдаст KeyError при пустом значении.
    if not user or not verify_password(username, password):
        raise HTTPException(status_code=403, detail="Access forbidden")
    response = TEMPLATES.TemplateResponse("form_accepted.html", {"request": request, "user": USERS[username]['name'], "balance": USERS[username]['balance']},)
    # кодирует пользователя в base64 и подписывает данные(hmac)
    username_signed = create_user_cookie(username)
    # записывает куку с пользователем
    response.set_cookie(key="username", value=username_signed)
    return response


@router.get("/unify_phone_from_query")
def phone_from_query(*, phone: Optional[str] = Query(None, example="89991234567")):
    raw_phone = phone
    resp_phone = validate_phone(raw_phone)
    return Response(resp_phone)


@router.get("/coin/", status_code=200)
def request_coin(request: Request):
    return TEMPLATES.TemplateResponse("form.html", {"request": request},)


@router.post("/request/coin/", status_code=201)
def post_request_coin(coin: str = Form(...), currency: str = Form(...)):
    payload = {'ids': coin, 'vs_currencies': currency}
    r = requests.get('https://api.coingecko.com/api/v3/simple/price', params=payload)
#    coin_list = requests.get('https://api.coingecko.com/api/v3/coins/list').json()
#    with open("coin.json", "a") as c:
#        json.dump(coin_list, c)
#    currencies_list = requests.get('https://api.coingecko.com/api/v3/simple/supported_vs_currencies').json()
#    with open("currencies.json", "a") as c:
#        json.dump(currencies_list, c)
    return r.json()

app.include_router(router)


