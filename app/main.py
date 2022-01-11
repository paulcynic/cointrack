from time import time
from fastapi import FastAPI, APIRouter, Cookie, Form, HTTPException, Request, Depends
from fastapi.responses import Response, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from sqlalchemy.orm import Session

from typing import Optional

from app import crud
from app.api import deps
from app.user_data import USERS
from app.api.api_v1.api import api_router
from app.core.config import settings
from app.validators import get_username_from_signed_string, verify_password, create_user_cookie


app = FastAPI(title="DemoAuthCointrack", openapi_url="/openapi.json")
root_router = APIRouter()

TEMPLATES = Jinja2Templates(directory=str(settings.BASE_PATH/"templates"))
app.mount("/static", StaticFiles(directory=str(settings.BASE_PATH/"static")), name="static")

# читает куку "username" как параметр функции
@root_router.get("/login/", status_code=200) #response_model=User
def index_page(request: Request, response: Response, username: Optional[str] = Cookie(default=None)):
    login_page = TEMPLATES.TemplateResponse("login.html", {"request": request},)
    if username is None:
        return login_page
    try:
        get_username_from_signed_string(username)
    except ValueError:
        response = login_page
        response.delete_cookie("username")
        return response
    url = app.url_path_for("root")
    response = RedirectResponse(url=url)
    return response


@root_router.post("/login/", status_code=201)
def process_login_page(*, response: Response, username: str = Form(...), password: str = Form(...)):
    user = USERS.get(username)
    #Если не найдёт ключ, вернёт пустое значение
    #user = users[username] выдаст KeyError при пустом значении.
    if not user or not verify_password(username, password):
        raise HTTPException(status_code=403, detail="Access forbidden")
    username_signed = create_user_cookie(username)
    # записывает куку с пользователем
    response.set_cookie(key="username", value=username_signed)
    return {"response": "Congratulations! You are logged in."}


@root_router.get("/", status_code=200)
def root(*,
        request: Request,
        db: Session = Depends(deps.get_db)
        ):
    coins = crud.coin.get_multi(db=db, limit=4)
    currencies = crud.currency.get_multi(db=db, limit=5)
    return TEMPLATES.TemplateResponse("index.html", {
        "request": request,
        "coins": coins,
        "currencies": currencies
        })


# Add time of the request to the headers.
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time()
    response = await call_next(request)
    process_time = time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


app.include_router(api_router, prefix=settings.API_V1_STR)
app.include_router(root_router)

