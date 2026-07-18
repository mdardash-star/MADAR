from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_employees_route_is_accessible() -> None:
    response = client.get("/api/v1/hr/employees", params={"company_id": 1})
    assert response.status_code == 200


def test_attendance_route_is_accessible() -> None:
    response = client.get("/api/v1/hr/attendances", params={"company_id": 1})
    assert response.status_code == 200


def test_payroll_route_is_accessible() -> None:
    response = client.get("/api/v1/hr/payrolls", params={"company_id": 1})
    assert response.status_code == 200
