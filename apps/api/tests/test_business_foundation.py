from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_cost_centers_route_is_accessible() -> None:
    response = client.get("/api/v1/business-foundation/cost-centers", params={"company_id": 1})
    assert response.status_code == 200


def test_customer_groups_route_is_accessible() -> None:
    response = client.get("/api/v1/business-foundation/customer-groups", params={"company_id": 1})
    assert response.status_code == 200


def test_brands_route_is_accessible() -> None:
    response = client.get("/api/v1/business-foundation/brands", params={"company_id": 1})
    assert response.status_code == 200
