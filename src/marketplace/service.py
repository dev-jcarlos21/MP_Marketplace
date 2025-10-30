import pandas as pd
from loguru import logger
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from marketplace.database import init_db
from marketplace.settings import settings
from utils.safe_db import SafeDB

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()
helpers = SafeDB(db)


def init_db_marketplace():
    """Inicializa tablas en DB."""
    init_db()


def get_db_marketplace():
    sql = """
        SELECT sku,
               name,
               category,
               price,
               stock
        FROM mkp_mini.productos
    """
    try:
        res = helpers.safe_execute(sql)
        rows = res.fetchall()
        csv_file = pd.DataFrame(rows)
        csv_file.to_csv(settings.PRODUCTS_PATH, header=True, index=False)
        logger.info(
            f"""Productos cargados: {csv_file}
            Archivo guardado en: {settings.PRODUCTS_PATH}
            """
        )
    finally:
        db.close()
