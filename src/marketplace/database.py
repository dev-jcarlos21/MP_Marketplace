from loguru import logger
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from marketplace.orm import Base
from marketplace.settings import settings

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


def init_db():
    logger.info("Inicializando base de datos")
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
