import os
from pydantic import AnyHttpUrl, BaseSettings, validator
from typing import List, Optional, Union
from pathlib import Path

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    BASE_PATH = Path(__file__).resolve().parent.parent
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    BOT_CHAT_ID = os.getenv('BOT_CHAT_ID')

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    SQLALCHEMY_DATABASE_URI: Optional[str] = "postgresql+psycopg2://paulcynic@localhost/cointrack_db"
    FIRST_SUPERUSER: str = "paul@user.com"
    URL_SIMPLE_PRICE = 'https://api.coingecko.com/api/v3/simple/price'

    class Config:
        case_sensitive = True


settings = Settings()
