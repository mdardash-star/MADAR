from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_endpoint() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_login_requires_credentials() -> None:
    response = client.post("/auth/login", json={"email": "", "password": ""})
    assert response.status_code == 422
