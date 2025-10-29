from typing import Any

import requests
from loguru import logger
from requests.exceptions import RequestException

from db import Base
from db.session import Engine, Session
from utils.safe_db import SafeDB

from .settings import settings

db = Session()
helpers = SafeDB(db)

FIELDS = ["sku", "name", "category", "price", "stock"]


def init_db():
    Base.metadata.create_all(bind=Engine)


def _request_catalog() -> Any:
    logger.debug("GET: " + settings.PRODUCTS_PATH)
    while True:
        try:
            res = requests.get(settings.PRODUCTS_PATH, timeout=60, verify=True)
            res.raise_for_status()
            return res.json()
        except RequestException as err:
            return helpers.log_and_exit(f"Error al realizar petición a: {err}")


def get_db_mkp_mini() -> None:
    try:
        return logger.success("Descarga finalizado")
    except RequestException as err:
        return helpers.log_and_exit(f"Error al realizar petición a: {err}")
