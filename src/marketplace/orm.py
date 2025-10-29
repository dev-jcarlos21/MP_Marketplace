from typing import TYPE_CHECKING

from sqlalchemy import DECIMAL, Column, Integer, String

from db import Base

if TYPE_CHECKING:
    pass


class MkpProduct(Base):
    __tablename__ = "productos"
    table_args = {"schema": "mpk_mini"}
    sku = Column(String(30), nullable=False, primary_key=True)
    name = Column(String(255), nullable=False)
    category = Column(String(255), nullable=False)
    price = Column(DECIMAL(8, 2), nullable=False)
    stock = Column(Integer, nullable=False)
