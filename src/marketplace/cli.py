from __future__ import annotations

import argparse
from pathlib import Path

from .logic import compute_order_totals, top_seller_by_revenue
from .repository import InMemoryRepo


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="CLI Marketplace (local, sin API)")
    parser.add_argument(
        "--products", type=Path, default=Path("/opt/marketplace-mini/data/productos.csv")
    )
    parser.add_argument(
        "--sellers", type=Path, default=Path("/opt/marketplace-mini/data/sellers.json")
    )
    parser.add_argument(
        "--orders", type=Path, default=Path("/opt/marketplace-mini/data/orders.json")
    )
    parser.add_argument(
        "--task", choices=["validate", "totals", "top-seller"], default="validate"
    )
    return parser
def main() -> int:
    args = build_parser().parse_args()
    repo = InMemoryRepo()
    # Cargas
    repo.load_products_csv(args.products)
    repo.load_sellers_json(args.sellers)
    repo.load_orders_json(args.orders)

    if args.task == "validate":
        print(
            f"Productos: {len(repo.products)} "
            f"| Sellers: {len(repo.sellers)} "
            f"| Órdenes: {len(repo.orders)}"
        )
        oos = repo.out_of_stock()
        print(f"Agotados: {len(oos)}")
        return 0

    if args.task == "totals":
        for order in repo.orders.values():
            totals = compute_order_totals(order, repo)
            print(
                f"{order.order_id}: subtotal={totals['subtotal']:.2f} "
                f"tax={totals['tax']:.2f} total={totals['total']:.2f}"
            )
            return 0

    if args.task == "top-seller":
        result = top_seller_by_revenue(repo.orders.values(), repo)
        if result is None:
            print("Sin datos")
        else:
            seller_id, revenue = result
            print(f"TOP vendedor: {seller_id} con ${revenue:.2f}")
            return 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
