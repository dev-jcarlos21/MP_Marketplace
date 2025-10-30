from __future__ import annotations

# import argparse
from typing import Any

import typer
from loguru import logger

from marketplace.logic import compute_order_totals, top_seller_by_revenue
from marketplace.repository import InMemoryRepo
from marketplace.settings import settings

app = typer.Typer(
    help="""CLI Marketplace (local, sin API)
    Ejemplo de ejecucion: comando + argumentos (productos sellers orders)""",
)


def lazy_load_func() -> Any:
    """Carga el módulo únicamente al ejecutar un comando."""
    import marketplace.service as marketplace

    return marketplace


@app.command()
def init_db():
    """Inicializa tablas en DB."""
    marketplace = lazy_load_func()
    marketplace.init_db()


@app.command()
def get_db_marketplace():
    """Actualizacion de productos en el archivo CSV."""
    marketplace = lazy_load_func()
    marketplace.get_db_marketplace()


# Funcion para cargar los datos desde los archivos
def load_repository(products: str, sellers: str, orders: str) -> InMemoryRepo:
    repo = InMemoryRepo()
    if products == "products":
        repo.load_products_csv(settings.PRODUCTS_PATH)
    if sellers == "sellers":
        repo.load_sellers_json(settings.SELLERS_PATH)
    if orders == "orders":
        repo.load_orders_json(settings.ORDERS_PATH)
    return repo


@app.command()
def validate(products: str, sellers: str, orders: str) -> int:
    repo = load_repository(products, sellers, orders)
    logger.success(
        f"Productos: {len(repo.products)} "
        f"| Sellers: {len(repo.sellers)} "
        f"| Órdenes: {len(repo.orders)}",
    )
    oos = repo.out_of_stock()
    logger.warning(f"Agotados: {len(oos)}")
    return 0


@app.command()
def totals(products: str, sellers: str, orders: str) -> int:
    repo = load_repository(products, sellers, orders)
    for order in repo.orders.values():
        totals_product = compute_order_totals(order, repo)
        logger.success(
            f"{order.order_id}: subtotal={totals_product['subtotal']:.2f} "
            f"tax={totals_product['tax']:.2f} total={totals_product['total']:.2f}",
        )
        return 0
    return 0


@app.command()
def top_seller(products: str, sellers: str, orders: str) -> int:
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


def main():
    app()


if __name__ == "__main__":
    raise SystemExit(main())
