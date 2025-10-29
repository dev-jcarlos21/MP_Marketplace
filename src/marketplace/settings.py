from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = ""
    PRODUCTS_PATH: str = ""
    SELLERS_PATH: str = ""
    ORDERS_PATH: str = ""

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
