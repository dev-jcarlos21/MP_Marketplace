from sqlalchemy import DECIMAL, Column, Integer, String
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class MkpProduct(Base):
    __tablename__ = "productos"
    table_args = {"schema": "mpk_mini"}
    sku = Column(String(30), nullable=False, primary_key=True)
    name = Column(String(255), nullable=False)
    category = Column(String(255), nullable=False)
    price = Column(DECIMAL(8, 2), nullable=False)
    stock = Column(Integer, nullable=False)
