from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_chart_of_accounts_route_is_accessible() -> None:
    response = client.get("/api/v1/finance/chart-of-accounts", params={"company_id": 1})
    assert response.status_code == 200


def test_journal_entries_route_is_accessible() -> None:
    response = client.get("/api/v1/finance/journal-entries", params={"company_id": 1})
    assert response.status_code == 200
