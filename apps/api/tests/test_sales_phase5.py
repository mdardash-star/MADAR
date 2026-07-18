from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_quotations_route_is_accessible() -> None:
    response = client.get("/api/v1/sales/quotations", params={"company_id": 1})
    assert response.status_code == 200


def test_sales_orders_route_is_accessible() -> None:
    response = client.get("/api/v1/sales/orders", params={"company_id": 1})
    assert response.status_code == 200


def test_sales_invoices_route_is_accessible() -> None:
    response = client.get("/api/v1/sales/invoices", params={"company_id": 1})
    assert response.status_code == 200
