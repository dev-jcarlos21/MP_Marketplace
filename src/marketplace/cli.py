from __future__ import annotations

# import argparse
from pathlib import Path

import typer
from loguru import logger

from .logic import compute_order_totals, top_seller_by_revenue
from .repository import InMemoryRepo
from .settings import settings

app = typer.Typer(
    help="""CLI Marketplace (local, sin API)
    Ejemplo de ejecucion: comando + argumentos (productos sellers orders)"""
)

# Funcion para cargar los datos desde los archivos
def load_repository(products: str, sellers: str, orders: str) -> InMemoryRepo:
    repo = InMemoryRepo()
    if products == "products":
        products = Path(settings.PRODUCTS_PATH)
    if sellers == "sellers":
        sellers = Path(settings.SELLERS_PATH)
    if orders == "orders":
        orders = Path(settings.ORDERS_PATH)
    repo.load_products_csv(products)
    repo.load_sellers_json(sellers)
    repo.load_orders_json(orders)
    return repo

@app.command()
def validate (products: str, sellers: str, orders: str) -> int:
    repo = load_repository(products, sellers, orders)
    logger.success(
        f"Productos: {len(repo.products)} "
        f"| Sellers: {len(repo.sellers)} "
        f"| Órdenes: {len(repo.orders)}"
    )
    oos = repo.out_of_stock()
    logger.warning(f"Agotados: {len(oos)}")
    return 0

@app.command()
def totals (products: str, sellers: str, orders: str) -> int:
    repo = load_repository(products, sellers, orders)
    for order in repo.orders.values():
        totals = compute_order_totals(order, repo)
        logger.success(
            f"{order.order_id}: subtotal={totals['subtotal']:.2f} "
            f"tax={totals['tax']:.2f} total={totals['total']:.2f}"
        )
        return 0

@app.command()
def top_seller (products: str, sellers: str, orders: str) -> int:
    repo = load_repository(products, sellers, orders)
    result = top_seller_by_revenue(repo.orders.values(), repo)
    if result is None:
        logger.warning("Sin datos")
    else:
        seller_id, revenue = result
        logger.success(f"TOP vendedor: {seller_id} con ${revenue:.2f}")
        return 0
    oos = repo.out_of_stock()
    logger.warning(f"Agotados: {len(oos)}")
    return 0

def main() -> None:
    app()

if __name__ == "__main__":
    raise SystemExit(main())
