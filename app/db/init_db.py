import logging
import json
from sqlalchemy.orm import Session

from app import crud, schemas

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

FIRST_SUPERUSER = "paul@user.com"

# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28


def init_db(db: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    # Base.metadata.create_all(bind=engine)
    if FIRST_SUPERUSER:
        user = crud.user.get_by_name(db, name=FIRST_SUPERUSER)
        if not user:
            user_in = schemas.UserCreate(
                name=FIRST_SUPERUSER,
                password="some_password_1",
                balance=0,
                is_superuser=True,
            )
            user = crud.user.create(db, obj_in=user_in)  # noqa: F841
        else:
            logger.warning(
                "Skipping creating superuser. User with email "
                f"{FIRST_SUPERUSER} already exists. "
            )
        currency = crud.currency.get_multi(db, limit=10)
        if not currency:
            with open("/home/paulcynic/cointrack/currencies.json", "r", encoding="utf-8") as currency_db:
                currencies = json.load(currency_db)
                for row in range(len(currencies)):
                    currency_in = schemas.CurrencyCreate(
                            label = currencies[row]
                        )
                    crud.currency.create(db, obj_in=currency_in)
    else:
        logger.warning(
            "Skipping creating superuser.  FIRST_SUPERUSER needs to be "
            "provided as an env variable. "
            "e.g.  FIRST_SUPERUSER=admin@api.coursemaker.io"
        )
