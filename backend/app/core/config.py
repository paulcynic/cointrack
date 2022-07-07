import os
import pathlib
from pydantic import AnyHttpUrl, BaseSettings, validator
from typing import List, Optional, Union
from pathlib import Path

# Project Directories
ROOT = pathlib.Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    BASE_PATH = Path(__file__).resolve().parent.parent
    TELEGRAM_BOT_TOKEN: Optional[str] = os.getenv('TELEGRAM_BOT_TOKEN')
    BOT_CHAT_ID: Optional[str] = os.getenv('BOT_CHAT_ID')
    JWT_SECRET: Optional[str] = os.getenv('SECRET_KEY')
    ALGORITHM: str = "HS256"
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 180

    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = [
        "http://localhost:3000",
        "http://localhost:3001",  # type: ignore
        "http://localhost:8002",
        "http://localhost:8001",  # type: ignore
    ]

    # Origins that match this regex OR are in the above list are allowed
    BACKEND_CORS_ORIGIN_REGEX: Optional[
        str
    ] = "https.*\.(netlify.app|herokuapp.com)"  # noqa: W605


    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    SQLALCHEMY_DATABASE_URI: Optional[str] = "postgresql+psycopg2://fedora:fedora@127.0.0.1/cointrack_db"
    FIRST_SUPERUSER: str = "user@user.com"
    FIRST_SUPERUSER_PW: str = "password"

    URL_SIMPLE_PRICE: str = 'https://api.coingecko.com/api/v3/simple/price'
    LOG_LEVEL: str = 'INFO'
    LOG_TRACEBACK: bool = False

    class Config:
        case_sensitive = True


settings = Settings()
