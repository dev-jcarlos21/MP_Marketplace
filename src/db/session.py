from sqlalchemy import create_engine as _create_engine
from sqlalchemy import inspect
from sqlalchemy.orm import sessionmaker

from marketplace.settings import settings

Session = sessionmaker(autocommit=False, autoflush=False)
Engine = _create_engine(settings.DATABASE_URL)
Inspector = inspect(Engine)
Session.configure(bind=Engine)
create_engine = _create_engine
