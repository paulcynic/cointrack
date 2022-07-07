import logging
import json
from sqlalchemy.orm import Session

from app import crud, schemas
from app.core.config import settings
from app.models import Coin, Currency

# from sqlalchemy import create_engine

# from postgresql import psycopg2
# engine = create_engine('postgresql+psycopg2://pg_user:pq_password@localhost:5432/mydatabase')


# SQLALCHEMY_DATABASE_URI = "sqlite:///example.db"
# 
# 
# engine = create_engine(
#     SQLALCHEMY_DATABASE_URI,
#     # required for sqlite
#     connect_args={"check_same_thread": False},
# )


logger = logging.getLogger(__name__)

# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28


def init_db(db: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    # Base.metadata.create_all(bind=engine)
    if settings.FIRST_SUPERUSER:
        superuser = crud.user.get_by_email(db, email=settings.FIRST_SUPERUSER)
        if not superuser:
            user_in = schemas.UserCreate(
                full_name="Initial Super User",
                email=settings.FIRST_SUPERUSER,
                password=settings.FIRST_SUPERUSER_PW,
                is_superuser=True,
            )
            superuser = crud.user.create(db, obj_in=user_in)  # noqa: F841
        else:
            logger.warning(
                "Skipping creating superuser. User with email "
                f"{settings.FIRST_SUPERUSER} already exists. "
            )
        currencies = db.query(Currency).first()
        if not currencies:
            with open("currencies.json", "r", encoding="utf-8") as currency_db:
                currencies = json.load(currency_db)
                for i in range(len(currencies)):
                    currency_in = schemas.CurrencyCreate(
                            label = currencies[i]
                        )
                    crud.currency.create(db, obj_in=currency_in)
        coins = db.query(Coin).first()
        if not coins:
            with open("coins.json", "r", encoding="utf-8") as coin_db:
                coins = json.load(coin_db)
                for i in range(len(coins)):
                    coin_in = schemas.CoinCreate(
                            name = coins[i]
                        )
                    crud.coin.create(db, obj_in=coin_in)
    else:
        logger.warning(
            "Skipping creating superuser.  FIRST_SUPERUSER needs to be "
            "provided as an env variable. "
            "e.g.  FIRST_SUPERUSER=admin@api.mail.io"
        )
