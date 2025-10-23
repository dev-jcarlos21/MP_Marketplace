from marketplace.logic import compute_item_total, compute_order_totals
from marketplace.models import Order, OrderItem, Product, Seller
from marketplace.repository import InMemoryRepo


def make_repo() -> InMemoryRepo:
    repo = InMemoryRepo()
    repo.products["SKU-001"] = Product(sku="SKU-001", name="X", category="C", price=100.0, stock=5)
    repo.products["SKU-002"] = Product(sku="SKU-002", name="Y", category="C", price=50.0, stock=0)
    repo.sellers["S-1"] = Seller(seller_id="S-1", display_name="Demo", rating=4.0)
    return repo


def test_compute_item_total():
    repo = make_repo()
    p = repo.products["SKU-001"]
    assert compute_item_total(p, 2, 0.10) == 180.00  # 100*2*(1-0.1) = 180.0


def test_compute_order_totals_ignores_missing_or_oos():
    repo = make_repo()
    order = Order(
        order_id="O-1",
        seller_id="S-1",
        items=[
            OrderItem(sku="SKU-001", quantity=2, discount=0.0),  # válido
            OrderItem(sku="SKU-XXX", quantity=1, discount=0.0),  # SKU inexistente
            OrderItem(sku="SKU-002", quantity=1, discount=0.0),  # stock=0
        ],
        tax_rate=0.16,
    )
    totals = compute_order_totals(order, repo)
    assert round(totals["subtotal"], 2) == 200.00
    assert round(totals["tax"], 2) == 32.00
    assert round(totals["total"], 2) == 232.00
