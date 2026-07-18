from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_purchase_orders_route_is_accessible() -> None:
    response = client.get("/api/v1/procurement/purchase-orders", params={"company_id": 1})
    assert response.status_code == 200


def test_goods_receipts_route_is_accessible() -> None:
    response = client.get("/api/v1/procurement/goods-receipts", params={"company_id": 1})
    assert response.status_code == 200


def test_purchase_returns_route_is_accessible() -> None:
    response = client.get("/api/v1/procurement/purchase-returns", params={"company_id": 1})
    assert response.status_code == 200
