"""
MADAR Release v0.1 — Full Release Verification Suite

Covers every requirement for the v0.1 release gate:
  ✅ Company registration (bootstraps admin user)
  ✅ Login → JWT access token
  ✅ Authenticated /auth/me
  ✅ Dashboard data endpoint (API status)
  ✅ CRUD: Customers
  ✅ CRUD: Suppliers
  ✅ CRUD: Products (with category + UoM dependency)
  ✅ CRM Leads (smoke)
  ✅ Sales Quotations (smoke)
  ✅ Inventory stock movements (smoke)
"""

import uuid
import warnings

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


# ── Fixtures ──────────────────────────────────────────────────────────────────

def _uid() -> str:
    """Return a short random hex string suitable for unique codes."""
    return uuid.uuid4().hex[:8]


def _slug() -> str:
    return f"rel01-{_uid()}"


def _register_company():
    """Register a fresh company and return (company_id, admin_email)."""
    slug = _slug()
    email = f"admin+{slug}@example.com"
    resp = client.post(
        "/companies/register",
        json={
            "company_name": f"MADAR Release Test {slug}",
            "company_slug": slug,
            "admin_email": email,
            "admin_password": "Release2026",
            "admin_full_name": "Release Admin",
        },
    )
    assert resp.status_code == 200, f"Registration failed: {resp.text}"
    company_id = resp.json()["company"]["id"]
    return company_id, email


def _login(email: str, password: str = "Release2026") -> str:
    resp = client.post("/auth/login", json={"email": email, "password": password})
    assert resp.status_code == 200, f"Login failed: {resp.text}"
    return resp.json()["access_token"]


def _auth_headers(email: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {_login(email)}"}


# ── REQ-1  Health check ───────────────────────────────────────────────────────

def test_health_endpoint():
    """The /health endpoint returns 200 with status healthy."""
    resp = client.get("/health")
    assert resp.status_code == 200
    body = resp.json()
    assert body.get("status") in ("ok", "healthy")


def test_root_endpoint():
    """The / root endpoint identifies the application."""
    resp = client.get("/")
    assert resp.status_code == 200
    assert resp.json().get("name") == "MADAR ERP API"


# ── REQ-2  Company creation ───────────────────────────────────────────────────

def test_company_registration():
    """POST /companies/register creates company and bootstraps admin user."""
    slug = _slug()
    resp = client.post(
        "/companies/register",
        json={
            "company_name": f"Test Co {slug}",
            "company_slug": slug,
            "admin_email": f"admin+{slug}@example.com",
            "admin_password": "Release2026",
            "admin_full_name": "Test Admin",
        },
    )
    assert resp.status_code == 200, resp.text
    data = resp.json()
    assert "company" in data
    assert data["company"]["slug"] == slug
    assert "admin" in data or "user" in data


def test_duplicate_slug_rejected():
    """Registering a company with an existing slug is rejected."""
    slug = _slug()
    payload = {
        "company_name": f"Co {slug}",
        "company_slug": slug,
        "admin_email": f"a+{slug}@example.com",
        "admin_password": "Release2026",
        "admin_full_name": "A",
    }
    r1 = client.post("/companies/register", json=payload)
    assert r1.status_code == 200

    payload["admin_email"] = f"b+{slug}@example.com"
    r2 = client.post("/companies/register", json=payload)
    assert r2.status_code == 400


# ── REQ-3  Login ──────────────────────────────────────────────────────────────

def test_login_returns_tokens():
    """POST /auth/login returns access_token and refresh_token."""
    company_id, email = _register_company()
    resp = client.post("/auth/login", json={"email": email, "password": "Release2026"})
    assert resp.status_code == 200, resp.text
    data = resp.json()
    assert "access_token" in data
    assert "refresh_token" in data


def test_login_wrong_password_rejected():
    """Wrong password returns 401."""
    company_id, email = _register_company()
    resp = client.post("/auth/login", json={"email": email, "password": "WrongPass"})
    assert resp.status_code == 401


def test_me_endpoint():
    """GET /auth/me returns current user token payload when authenticated."""
    company_id, email = _register_company()
    token = _login(email)
    resp = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200, resp.text
    data = resp.json()
    assert data.get("sub") == email or data.get("email") == email


def test_token_refresh():
    """POST /auth/refresh returns a new access token."""
    company_id, email = _register_company()
    login_resp = client.post("/auth/login", json={"email": email, "password": "Release2026"})
    refresh_token = login_resp.json()["refresh_token"]
    resp = client.post("/auth/refresh", json={"refresh_token": refresh_token})
    assert resp.status_code == 200, resp.text
    assert "access_token" in resp.json()


# ── REQ-4  Dashboard (API status) ────────────────────────────────────────────

def test_api_status_endpoint():
    """GET /api/v1/status returns ok — the dashboard API layer is reachable."""
    resp = client.get("/api/v1/status")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


# ── REQ-5a  CRUD: Customers ───────────────────────────────────────────────────

def test_customers_full_crud():
    """Create, read, update, archive a customer using authenticated routes."""
    company_id, email = _register_company()
    headers = _auth_headers(email)
    base = "/api/v1/master-data"

    create = client.post(
        f"{base}/customers",
        json={
            "company_id": company_id,
            "name": "Acme Corp",
            "code": f"ACME-{_uid()}",
            "email": "acme@example.com",
            "phone": "+966500000001",
        },
        headers=headers,
    )
    assert create.status_code == 201, create.text
    cust_id = create.json()["id"]

    lst = client.get(f"{base}/customers", params={"company_id": company_id}, headers=headers)
    assert lst.status_code == 200
    assert any(c["id"] == cust_id for c in lst.json())

    upd = client.put(
        f"{base}/customers/{cust_id}",
        json={"phone": "+966500000002"},
        headers=headers,
    )
    assert upd.status_code == 200
    assert upd.json()["phone"] == "+966500000002"

    dlt = client.delete(f"{base}/customers/{cust_id}", headers=headers)
    assert dlt.status_code == 200

    lst2 = client.get(f"{base}/customers", params={"company_id": company_id}, headers=headers)
    assert not any(c["id"] == cust_id for c in lst2.json())


# ── REQ-5b  CRUD: Suppliers ───────────────────────────────────────────────────

def test_suppliers_full_crud():
    """Create, read, update, delete a supplier."""
    company_id, email = _register_company()
    base = "/api/v1/master-data"

    create = client.post(
        f"{base}/suppliers",
        json={
            "company_id": company_id,
            "name": "Global Supplies LLC",
            "code": f"SUP-{_uid()}",
            "email": "supply@example.com",
        },
    )
    assert create.status_code == 201, create.text
    sup_id = create.json()["id"]

    lst = client.get(f"{base}/suppliers", params={"company_id": company_id})
    assert lst.status_code == 200
    assert any(s["id"] == sup_id for s in lst.json())

    upd = client.put(f"{base}/suppliers/{sup_id}", json={"phone": "+966500000099"})
    assert upd.status_code == 200

    dlt = client.delete(f"{base}/suppliers/{sup_id}")
    assert dlt.status_code == 200

    lst2 = client.get(f"{base}/suppliers", params={"company_id": company_id})
    assert not any(s["id"] == sup_id for s in lst2.json())


# ── REQ-5c  CRUD: Products ────────────────────────────────────────────────────

def _setup_product_deps(company_id: int) -> tuple[int, int]:
    """Create a category and UoM, return (category_id, uom_id)."""
    base = "/api/v1/master-data"
    cat = client.post(
        f"{base}/product-categories",
        json={"company_id": company_id, "name": "Electronics", "code": f"EL-{_uid()}"},
    )
    assert cat.status_code == 201, cat.text

    uom = client.post(
        f"{base}/units-of-measure",
        json={"company_id": company_id, "name": "Piece", "code": f"PC-{_uid()}", "abbreviation": "pc"},
    )
    assert uom.status_code == 201, uom.text

    return cat.json()["id"], uom.json()["id"]


def test_products_full_crud():
    """Create, read, update, delete a product."""
    company_id, email = _register_company()
    base = "/api/v1/master-data"
    cat_id, uom_id = _setup_product_deps(company_id)

    create = client.post(
        f"{base}/products",
        json={
            "company_id": company_id,
            "name": "Laptop Pro",
            "sku": f"LP-{_slug()[:8]}",
            "selling_price": 2999.99,
            "cost_price": 1800.00,
            "category_id": cat_id,
            "unit_of_measure_id": uom_id,
        },
    )
    assert create.status_code == 201, create.text
    prod_id = create.json()["id"]

    lst = client.get(f"{base}/products", params={"company_id": company_id})
    assert lst.status_code == 200
    assert any(p["id"] == prod_id for p in lst.json())

    upd = client.put(f"{base}/products/{prod_id}", json={"selling_price": 2799.99})
    assert upd.status_code == 200
    assert upd.json()["selling_price"] == 2799.99

    dlt = client.delete(f"{base}/products/{prod_id}")
    assert dlt.status_code == 200

    lst2 = client.get(f"{base}/products", params={"company_id": company_id})
    assert not any(p["id"] == prod_id for p in lst2.json())


# ── REQ-6  Regression — CRM, Sales, Inventory smoke ──────────────────────────

def test_crm_leads_smoke():
    company_id, _ = _register_company()
    resp = client.get("/api/v1/crm/leads", params={"company_id": company_id})
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


def test_sales_quotations_smoke():
    company_id, _ = _register_company()
    resp = client.get("/api/v1/sales/quotations", params={"company_id": company_id})
    assert resp.status_code == 200


def test_inventory_stock_movements_smoke():
    company_id, _ = _register_company()
    resp = client.get("/api/v1/inventory/stock-movements", params={"company_id": company_id})
    assert resp.status_code == 200


def test_finance_chart_of_accounts_smoke():
    company_id, _ = _register_company()
    resp = client.get("/api/v1/finance/chart-of-accounts", params={"company_id": company_id})
    assert resp.status_code == 200


def test_hr_employees_smoke():
    company_id, _ = _register_company()
    resp = client.get("/api/v1/hr/employees", params={"company_id": company_id})
    assert resp.status_code == 200


def test_assets_smoke():
    company_id, _ = _register_company()
    resp = client.get("/api/v1/assets/fixed-assets", params={"company_id": company_id})
    assert resp.status_code == 200


def test_no_utcnow_deprecation_warning_in_crud_flows():
    """Guard against reintroducing datetime.utcnow() in CRUD write/delete paths."""
    company_id, email = _register_company()
    headers = _auth_headers(email)
    base = "/api/v1/master-data"

    with warnings.catch_warnings(record=True) as captured:
        warnings.simplefilter("always", DeprecationWarning)

        customer = client.post(
            f"{base}/customers",
            json={
                "company_id": company_id,
                "name": "Deprecation Guard Customer",
                "code": f"DG-CUS-{_uid()}",
            },
            headers=headers,
        )
        assert customer.status_code == 201, customer.text
        customer_id = customer.json()["id"]
        assert client.delete(f"{base}/customers/{customer_id}", headers=headers).status_code == 200

        supplier = client.post(
            f"{base}/suppliers",
            json={
                "company_id": company_id,
                "name": "Deprecation Guard Supplier",
                "code": f"DG-SUP-{_uid()}",
            },
        )
        assert supplier.status_code == 201, supplier.text
        supplier_id = supplier.json()["id"]
        assert client.delete(f"{base}/suppliers/{supplier_id}").status_code == 200

        category = client.post(
            f"{base}/product-categories",
            json={"company_id": company_id, "name": "DG Category", "code": f"DG-CAT-{_uid()}"},
        )
        assert category.status_code == 201, category.text

        uom = client.post(
            f"{base}/units-of-measure",
            json={"company_id": company_id, "name": "DG Piece", "code": f"DG-UOM-{_uid()}", "abbreviation": "pc"},
        )
        assert uom.status_code == 201, uom.text

        product = client.post(
            f"{base}/products",
            json={
                "company_id": company_id,
                "name": "Deprecation Guard Product",
                "sku": f"DG-SKU-{_uid()}",
                "cost_price": 10.0,
                "selling_price": 12.5,
                "category_id": category.json()["id"],
                "unit_of_measure_id": uom.json()["id"],
            },
        )
        assert product.status_code == 201, product.text
        product_id = product.json()["id"]
        assert client.delete(f"{base}/products/{product_id}").status_code == 200

    utcnow_warnings = [
        w for w in captured
        if issubclass(w.category, DeprecationWarning) and "utcnow" in str(w.message)
    ]
    assert not utcnow_warnings, [str(w.message) for w in utcnow_warnings]
