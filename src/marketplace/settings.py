from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PRODUCTS_PATH: Path
    SELLERS_PATH: Path
    ORDERS_PATH: Path

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
