from __future__ import annotations

from typing import Annotated

from pydantic import BaseModel, Field, field_validator
from pydantic.functional_validators import BeforeValidator
from typing_extensions import TypedDict

# --- Modelos Pydantic ---
PositiveFloat = Annotated[float, Field(ge=0)]
PositiveInt = Annotated[int, Field(ge=0)]
NonEmptyStr = Annotated[str, BeforeValidator(str.strip), Field(min_length=1)]


class Product(BaseModel):
    sku: NonEmptyStr
    name: NonEmptyStr
    category: NonEmptyStr
    price: PositiveFloat
    stock: PositiveInt

    @field_validator("sku")
    @classmethod
    def sku_format(cls, v: str) -> str:
        # Regla simple: SKU-XXX
        if not v.startswith("SKU-"):
            raise ValueError("SKU inválido: debe iniciar con 'SKU-'")
        return v


class ResponseProducts(BaseModel):
    res_products: list[Product]


class Seller(BaseModel):
    seller_id: NonEmptyStr
    display_name: NonEmptyStr
    rating: Annotated[float, Field(ge=0, le=5)]


class OrderItem(BaseModel):
    sku: NonEmptyStr
    quantity: Annotated[int, Field(ge=1)]
    discount: Annotated[float, Field(ge=0, le=0.90)] = 0.0  # 0 - 90%


class Order(BaseModel):
    order_id: NonEmptyStr
    seller_id: NonEmptyStr
    items: list[OrderItem]
    tax_rate: Annotated[float, Field(ge=0, le=0.30)] = 0.16


# --- Tipos auxiliares para reportes (no obligatorios, pero útiles) ---


class OrderTotals(TypedDict):
    order_id: str
    subtotal: float
    tax: float
    total: float
