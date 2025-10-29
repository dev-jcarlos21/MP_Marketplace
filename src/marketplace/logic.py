from __future__ import annotations

import operator
from collections.abc import Iterable

from .models import Order, OrderTotals, Product
from .repository import InMemoryRepo


def compute_item_total(product: Product, quantity: int, discount: float) -> float:
    """
    Total por línea = price * quantity * (1 - discount)
    Redondea a 2 decimales al final.
    """
    return round(product.price * quantity * (1 - discount), 2)


def compute_order_totals(order: Order, repo: InMemoryRepo) -> OrderTotals:
    """
    Calcula subtotal, impuesto y total de una orden.
    - Ignora items con SKU inexistente o stock insuficiente (quantity > stock).
    - No modifica el stock (solo cálculo).
    """
    subtotal = 0.0

    for item in order.items:
        product = repo.get_product(item.sku)
        if product is None:
            continue
        if item.quantity > product.stock:
            continue

        item_total = compute_item_total(product, item.quantity, item.discount)
        subtotal += item_total

    tax = subtotal * order.tax_rate
    total = subtotal + tax

    return OrderTotals(
        order_id=order.order_id,
        subtotal=subtotal,
        tax=tax,
        total=total,
    )


def top_seller_by_revenue(
    orders: Iterable[Order], repo: InMemoryRepo
) -> tuple[str, float] | None:
    """
    Retorna (seller_id, revenue_total) del vendedor con más ingresos.
    - Usa compute_order_totals para cada orden.
    - Si no hay órdenes válidas, retorna None.
    """
    seller_revenues: dict[str, float] = {}

    for order in orders:
        totals = compute_order_totals(order, repo)
        seller_id = order.seller_id
        revenue = totals["total"]

        if seller_id in seller_revenues:
            seller_revenues[seller_id] += revenue
        else:
            seller_revenues[seller_id] = revenue

    if not seller_revenues:
        return None

    # Encuentra el seller con mayor revenue
    top_seller = max(seller_revenues.items(), key=operator.itemgetter(1))
    return top_seller
