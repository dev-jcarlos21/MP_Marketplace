import sys
from contextlib import suppress
from typing import TYPE_CHECKING, Any

from loguru import logger
from sqlalchemy import text
from sqlalchemy.exc import OperationalError, SQLAlchemyError

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


class SafeDB:
    def __init__(self, db: "Session") -> None:
        self.db = db

    def log_and_exit(self, msg: str) -> None:
        with suppress(OperationalError, SQLAlchemyError):
            self.db.rollback()
        logger.error(msg)
        sys.exit(1)

    def safe_execute(self, sql: str) -> Any:
        try:
            return self.db.execute(text(sql))
        except (OperationalError, SQLAlchemyError) as err:
            self.log_and_exit(f"Error al ejecutar query: {sql}\n {err}")
            sys.exit(1)

    def log_and_notification(
        self,
        msg: str,
    ) -> None:
        with suppress(OperationalError, SQLAlchemyError):
            self.db.rollback()
        logger.error(msg)
