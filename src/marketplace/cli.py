from __future__ import annotations

# import argparse
from pathlib import Path

import typer
from loguru import logger

from .logic import compute_order_totals, top_seller_by_revenue
from .repository import InMemoryRepo
from .settings import settings

app = typer.Typer(help="CLI Marketplace (local, sin API)")


# def build_parser() -> argparse.ArgumentParser:
 # parser = argparse.ArgumentParser(description="CLI Marketplace (local, sin API)", add_help=False)
    # parser.add_argument(
    #     "--products", type=Path, default=settings.PRODUCTS_PATH
    # )
    # parser.add_argument(
    #     "--sellers", type=Path, default=settings.SELLERS_PATH
    # )
    # parser.add_argument(
    #     "--orders", type=Path, default=settings.ORDERS_PATH
    # )
    # parser.add_argument(
    #     "--task", choices=["validate", "totals", "top-seller"], default="validate"
    # )
    # return parser

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

# def main() -> int:
    # args = build_parser().parse_args()
    # repo = InMemoryRepo()
    # # Cargas
    # repo.load_products_csv(args.products)
    # repo.load_sellers_json(args.sellers)
    # repo.load_orders_json(args.orders)

    # if args.task == "validate":
    #     logger.success(
    #         f"Productos: {len(repo.products)} "
    #         f"| Sellers: {len(repo.sellers)} "
    #         f"| Órdenes: {len(repo.orders)}"
    #     )
    #     oos = repo.out_of_stock()
    #     logger.warning(f"Agotados: {len(oos)}")
    #     return 0

    # if args.task == "totals":
    #     for order in repo.orders.values():
    #         totals = compute_order_totals(order, repo)
    #         logger.success(
    #             f"{order.order_id}: subtotal={totals['subtotal']:.2f} "
    #             f"tax={totals['tax']:.2f} total={totals['total']:.2f}"
    #         )
    #         return 0

    # if args.task == "top-seller":
    #     result = top_seller_by_revenue(repo.orders.values(), repo)
    #     if result is None:
    #         logger.warning("Sin datos")
    #     else:
    #         seller_id, revenue = result
    #         logger.success(f"TOP vendedor: {seller_id} con ${revenue:.2f}")
    #         return 0
    # return 0

def main() -> None:
    app()

if __name__ == "__main__":
    raise SystemExit(main())
