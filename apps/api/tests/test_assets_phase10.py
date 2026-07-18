from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_fixed_assets_route_is_accessible() -> None:
    response = client.get("/api/v1/assets/fixed-assets", params={"company_id": 1})
    assert response.status_code == 200


def test_asset_assignments_route_is_accessible() -> None:
    response = client.get("/api/v1/assets/assignments", params={"company_id": 1})
    assert response.status_code == 200
