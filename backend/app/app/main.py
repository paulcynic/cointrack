from time import time
from fastapi import FastAPI, APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session

from typing import Any

from app import crud
from app.api import deps
from app.api.api_v1.api import api_router
from app.core.config import settings
from app.core.logging_config import setup_logging


app = FastAPI(title="DemoAuthCointrack", openapi_url="/openapi.json")
root_router = APIRouter()

TEMPLATES = Jinja2Templates(directory=str(settings.BASE_PATH/"templates"))
app.mount(
    "/static", StaticFiles(directory=str(settings.BASE_PATH/"static")), name="static")

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin)
                       for origin in settings.BACKEND_CORS_ORIGINS],
        allow_origin_regex=settings.BACKEND_CORS_ORIGIN_REGEX,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@root_router.get("/", status_code=200)
def root(*,
         request: Request,
         db: Session = Depends(deps.get_db)
         ) -> Any:  # dict
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

#setup_logging()
