# MADAR ERP SaaS — Quick Start Guide

**Version**: v0.1  
**Time to first running system**: ~5 minutes

---

## Step 1 — Clone and configure

```bash
git clone https://github.com/mdardash-star/MADAR.git
cd MADAR

# Copy environment files
cp .env.example .env
cp apps/api/.env.example apps/api/.env
```

---

## Step 2 — Start the stack

```bash
docker compose up --build -d
```

Wait ~30 seconds for PostgreSQL to initialise, then:

```bash
docker compose exec api alembic upgrade head
```

---

## Step 3 — Load sample data (optional)

Load demo data for quick testing:

```bash
docker compose exec api sh -c "cd /app && PYTHONPATH=/app python scripts/seed_sample_data.py"
```

This creates:
- **Demo company**: ACME Corporation
- **Demo admin**: admin@acme-demo.com / Demo123!
- **Sample data**: 3 branches, 3 warehouses, 4 customers, 3 suppliers, 5 products, 2 quotations, 2 orders, 1 invoice

---

## Step 4 — Verify it's running

```bash
curl http://localhost:8000/health
# → {"status":"healthy"}
```

Open your browser:
- **Frontend**: http://localhost:3000
- **API docs**: http://localhost:8000/docs
- **Demo login** (if sample data loaded): admin@acme-demo.com / Demo123!

---

## Step 5 — Register your first company (manual option)

If you didn't load sample data above, you can create your own company:

---

## Step 5 — Register your first company (manual option)

If you didn't load sample data above, you can create your own company:

```bash
curl -s -X POST http://localhost:8000/companies/register \
  -H "Content-Type: application/json" \
  -d '{
    "company_name": "My Company",
    "company_slug": "my-company",
    "admin_email": "admin@mycompany.com",
    "admin_password": "SecurePass123",
    "admin_full_name": "System Admin"
  }' | python3 -m json.tool
```

Save the `company.id` from the response — you will need it for all subsequent API calls.

---

## Step 6 — Log in

```bash
curl -s -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@mycompany.com", "password": "SecurePass123"}' \
  | python3 -m json.tool
```

Copy the `access_token` from the response. Use it as a Bearer token for authenticated requests:

```bash
export TOKEN="<paste access_token here>"
```

---

## Step 7 — Create a customer

```bash
curl -s -X POST http://localhost:8000/api/v1/master-data/customers \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "company_id": 1,
    "name": "Acme Corporation",
    "code": "ACME-001",
    "email": "billing@acme.com",
    "phone": "+966500000001"
  }' | python3 -m json.tool
```

---

## Step 8 — Create a product

```bash
# First create a product category
curl -s -X POST http://localhost:8000/api/v1/master-data/product-categories \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"company_id": 1, "name": "Electronics", "code": "ELEC"}' | python3 -m json.tool

# Then create the product (use the category id from above)
curl -s -X POST http://localhost:8000/api/v1/master-data/products \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "company_id": 1,
    "name": "Laptop Pro 15",
    "sku": "LP15-001",
    "selling_price": 2999.99,
    "cost_price": 1800.00,
    "category_id": 1
  }' | python3 -m json.tool
```

---

## What you can do in v0.1

| Module | Available actions |
|--------|-----------------|
| Companies | Register, manage branches |
| Auth | Login, refresh token, view profile |
| Master Data | Customers, Suppliers, Products, Categories, UoM, Tax, Currency |
| Business Foundation | Brands, Cost Centers, Customer Groups, Contacts, Addresses |
| CRM | Leads, Pipelines, Stages, Opportunities, Activities, Notes |
| Sales | Quotations, Orders, Invoices |
| Purchasing | Purchase Orders, Goods Receipts, Purchase Returns |
| Inventory | Stock Movements, Transfers, Adjustments |
| Accounting | Chart of Accounts, Journal Entries |
| HR | Employees, Attendance, Payroll |
| Assets | Fixed Assets, Asset Assignments |

---

## Explore the API

All 156 endpoints are documented interactively:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## Stop the stack

```bash
docker compose down
```

---

## Need more details?

See [INSTALL.md](INSTALL.md) for the complete installation guide including production configuration and troubleshooting.
