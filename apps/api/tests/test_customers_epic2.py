import json
import uuid

from fastapi.testclient import TestClient

from app.core.database import SessionLocal
from app.main import app
from app.models.audit_log import AuditLog

client = TestClient(app)
BASE = "/api/v1/master-data/customers"


def _uid() -> str:
    return uuid.uuid4().hex[:10]


def _register() -> tuple[int, dict[str, str]]:
    suffix = _uid()
    email = f"customer-admin-{suffix}@example.com"
    response = client.post(
        "/companies/register",
        json={
            "company_name": f"Customer Test {suffix}",
            "company_slug": f"customer-test-{suffix}",
            "admin_email": email,
            "admin_password": "Customer2026!",
            "admin_full_name": "Customer Admin",
        },
    )
    assert response.status_code == 200, response.text
    company_id = response.json()["company"]["id"]
    login = client.post("/auth/login", json={"email": email, "password": "Customer2026!"})
    assert login.status_code == 200, login.text
    return company_id, {"Authorization": f"Bearer {login.json()['access_token']}"}


def _create(company_id: int, headers: dict[str, str], **overrides):
    payload = {
        "company_id": company_id,
        "name": f"Customer {_uid()}",
        "code": f"C-{_uid()}",
        "customer_type": "company",
        "tax_number": f"TAX-{_uid()}",
        "credit_limit": 1000,
        "payment_terms_days": 30,
        "is_active": True,
        **overrides,
    }
    return client.post(BASE, json=payload, headers=headers)


def test_customers_require_authentication():
    response = client.get(BASE, params={"company_id": 1})
    assert response.status_code == 401


def test_customer_create_detail_update_archive_restore_and_filters():
    company_id, headers = _register()
    created = _create(company_id, headers, name="Riyadh Customer", customer_type="company")
    assert created.status_code == 201, created.text
    customer_id = created.json()["id"]

    details = client.get(f"{BASE}/{customer_id}", headers=headers)
    assert details.status_code == 200
    assert details.json()["contacts"] == []
    assert details.json()["addresses"] == []

    updated = client.put(
        f"{BASE}/{customer_id}",
        json={"credit_limit": 2500, "payment_terms_days": 45, "notes": "Priority"},
        headers=headers,
    )
    assert updated.status_code == 200
    assert updated.json()["credit_limit"] == 2500
    assert updated.json()["payment_terms_days"] == 45

    searched = client.get(
        BASE,
        params={"company_id": company_id, "search": "Riyadh", "customer_type": "company", "with_meta": True},
        headers=headers,
    )
    assert searched.status_code == 200
    assert searched.json()["total"] >= 1
    assert any(item["id"] == customer_id for item in searched.json()["items"])

    archived = client.delete(f"{BASE}/{customer_id}", headers=headers)
    assert archived.status_code == 200

    normal_list = client.get(BASE, params={"company_id": company_id}, headers=headers)
    assert all(item["id"] != customer_id for item in normal_list.json())

    archived_list = client.get(
        BASE,
        params={"company_id": company_id, "include_archived": True},
        headers=headers,
    )
    assert any(item["id"] == customer_id and item["is_deleted"] for item in archived_list.json())

    restored = client.post(f"{BASE}/{customer_id}/restore", headers=headers)
    assert restored.status_code == 200
    assert restored.json()["is_deleted"] is False


def test_company_scoped_code_and_tax_uniqueness():
    company_a, headers_a = _register()
    company_b, headers_b = _register()
    code = f"SHARED-{_uid()}"
    tax = f"VAT-{_uid()}"

    first = _create(company_a, headers_a, code=code, tax_number=tax)
    assert first.status_code == 201

    duplicate_code = _create(company_a, headers_a, code=code, tax_number=f"VAT-{_uid()}")
    assert duplicate_code.status_code == 409

    duplicate_tax = _create(company_a, headers_a, code=f"C-{_uid()}", tax_number=tax)
    assert duplicate_tax.status_code == 409

    other_tenant = _create(company_b, headers_b, code=code, tax_number=tax)
    assert other_tenant.status_code == 201, other_tenant.text


def test_tenant_isolation_hides_other_company_customers():
    company_a, headers_a = _register()
    company_b, headers_b = _register()
    created = _create(company_a, headers_a)
    assert created.status_code == 201
    customer_id = created.json()["id"]

    wrong_list = client.get(BASE, params={"company_id": company_a}, headers=headers_b)
    assert wrong_list.status_code == 404

    wrong_detail = client.get(f"{BASE}/{customer_id}", headers=headers_b)
    assert wrong_detail.status_code == 404

    wrong_update = client.put(f"{BASE}/{customer_id}", json={"name": "Compromised"}, headers=headers_b)
    assert wrong_update.status_code == 404

    wrong_archive = client.delete(f"{BASE}/{customer_id}", headers=headers_b)
    assert wrong_archive.status_code == 404

    original = client.get(f"{BASE}/{customer_id}", headers=headers_a)
    assert original.status_code == 200
    assert original.json()["name"] != "Compromised"
    assert original.json()["is_deleted"] is False


def test_customer_contacts_and_addresses_are_nested_and_scoped():
    company_a, headers_a = _register()
    company_b, headers_b = _register()
    created = _create(company_a, headers_a)
    assert created.status_code == 201
    customer_id = created.json()["id"]

    contact = client.post(
        f"{BASE}/{customer_id}/contacts",
        json={"full_name": "Sales Contact", "email": "sales@example.com", "is_primary": True},
        headers=headers_a,
    )
    assert contact.status_code == 201, contact.text

    address = client.post(
        f"{BASE}/{customer_id}/addresses",
        json={"label": "HQ", "address_type": "billing", "city": "Riyadh", "is_primary": True},
        headers=headers_a,
    )
    assert address.status_code == 201, address.text
    assert address.json()["address_type"] == "billing"

    details = client.get(f"{BASE}/{customer_id}", headers=headers_a)
    assert len(details.json()["contacts"]) == 1
    assert len(details.json()["addresses"]) == 1

    cross_contact = client.put(
        f"{BASE}/{customer_id}/contacts/{contact.json()['id']}",
        json={"full_name": "Hacked"},
        headers=headers_b,
    )
    assert cross_contact.status_code == 404

    cross_address = client.delete(
        f"{BASE}/{customer_id}/addresses/{address.json()['id']}",
        headers=headers_b,
    )
    assert cross_address.status_code == 404


def test_invalid_relation_ids_and_negative_financial_values_are_rejected():
    company_id, headers = _register()
    invalid_relation = _create(company_id, headers, branch_id=999999999)
    assert invalid_relation.status_code == 409

    negative_credit = _create(company_id, headers, credit_limit=-1)
    assert negative_credit.status_code == 422

    negative_terms = _create(company_id, headers, payment_terms_days=-1)
    assert negative_terms.status_code == 422


def test_customer_audit_records_create_update_and_archive():
    company_id, headers = _register()
    created = _create(company_id, headers)
    assert created.status_code == 201
    customer_id = created.json()["id"]
    assert client.put(f"{BASE}/{customer_id}", json={"phone": "+966500000123"}, headers=headers).status_code == 200
    assert client.delete(f"{BASE}/{customer_id}", headers=headers).status_code == 200

    db = SessionLocal()
    try:
        logs = db.query(AuditLog).filter(
            AuditLog.entity_type == "customer",
            AuditLog.entity_id == customer_id,
        ).order_by(AuditLog.id).all()
        events = [log.event for log in logs]
        assert "customer_created" in events
        assert "customer_updated" in events
        assert "customer_archived" in events
        for log in logs:
            details = json.loads(log.details or "{}")
            assert details.get("company_id") == company_id
            assert log.user_email
    finally:
        db.close()


def test_pagination_metadata_and_active_filter():
    company_id, headers = _register()
    assert _create(company_id, headers, is_active=True).status_code == 201
    assert _create(company_id, headers, is_active=False).status_code == 201

    active = client.get(
        BASE,
        params={"company_id": company_id, "is_active": True, "limit": 1, "with_meta": True},
        headers=headers,
    )
    assert active.status_code == 200
    body = active.json()
    assert body["limit"] == 1
    assert body["total"] >= 1
    assert len(body["items"]) <= 1
    assert all(item["is_active"] for item in body["items"])
