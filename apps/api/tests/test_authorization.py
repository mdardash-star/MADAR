from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_missing_token_is_rejected() -> None:
    response = client.get("/api/v1/me")
    assert response.status_code == 401
