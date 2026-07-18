from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_stock_movements_route_is_accessible() -> None:
    response = client.get("/api/v1/inventory/stock-movements", params={"company_id": 1})
    assert response.status_code == 200


def test_stock_transfers_route_is_accessible() -> None:
    response = client.get("/api/v1/inventory/stock-transfers", params={"company_id": 1})
    assert response.status_code == 200


def test_stock_adjustments_route_is_accessible() -> None:
    response = client.get("/api/v1/inventory/stock-adjustments", params={"company_id": 1})
    assert response.status_code == 200
