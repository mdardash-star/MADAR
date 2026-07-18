## Verification 01

### Status
Executed

### Exact Command Executed
```bash
bash verify/01_start_clean.sh
```

### Execution Duration
```text
START=2026-07-18T19:50:26+00:00
END=2026-07-18T19:50:57+00:00
DURATION_SECONDS=30.276
```

### Command Output
```text

========================================================
  MADAR — Clean Start Verification
  2026-07-18T19:50:27+00:00
========================================================
[1;33m  ▶[0m  Checking prerequisites...
[0;32m  ✓[0m  Prerequisites satisfied
[1;33m  ▶[0m  Tearing down existing containers and volumes...
 Container madar-redis-1  Removed
 Network madar_default  Removing
 Volume madar_postgres_data  Removing
 Network madar_default  Removed
 Volume madar_postgres_data  Removed
[0;32m  ✓[0m  Teardown complete
[1;33m  ▶[0m  Checking environment files...
[0;32m  ✓[0m  Environment files ready
[1;33m  ▶[0m  Building Docker images and starting services (this may take 2-5 minutes)...
 Container madar-redis-1  Creating
 Container madar-db-1  Creating
 Container madar-redis-1  Created
 Container madar-db-1  Created
 Container madar-api-1  Creating
 Container madar-api-1  Created
 Container madar-web-1  Creating
 Container madar-web-1  Created
 Container madar-redis-1  Starting
 Container madar-db-1  Starting
 Container madar-redis-1  Started
 Container madar-db-1  Started
 Container madar-db-1  Waiting
 Container madar-redis-1  Waiting
 Container madar-db-1  Healthy
 Container madar-redis-1  Healthy
 Container madar-api-1  Starting
 Container madar-api-1  Started
 Container madar-web-1  Starting
 Container madar-web-1  Started
[0;32m  ✓[0m  docker compose up --build -d completed
[1;33m  ▶[0m  Waiting for services to become healthy (up to 90 seconds)...
[0;32m  ✓[0m  PostgreSQL is healthy (attempt 1)
[0;32m  ✓[0m  Redis is healthy (attempt 1)
     waiting for API... (1/18)
[0;32m  ✓[0m  API is healthy (attempt 2)
[0;32m  ✓[0m  Web is healthy (attempt 1)
[1;33m  ▶[0m  Applying database migrations...
INFO  [alembic.runtime.migration] Running upgrade 20260718_000009 -> 20260718_000010, Add CRM tables — leads, pipelines, stages, opportunities, activities, notes
INFO  [alembic.runtime.migration] Running upgrade 20260718_000010 -> 20260718_000011, Add timestamps and soft-delete columns to companies and branches tables
INFO  [alembic.runtime.migration] Running upgrade 20260718_000011 -> 20260718_000012, Add missing timestamp and soft-delete columns to identity tables (roles, permissions, users)
INFO  [alembic.runtime.migration] Running upgrade 20260718_000012 -> 20260718_000013, Fix roles slug uniqueness — change global unique to per-company unique constraint
INFO  [alembic.runtime.migration] Running upgrade 20260718_000013 -> 20260718_000014, Add missing product columns (brand_id, image_url) and create audit_logs + tenants tables
[0;32m  ✓[0m  Migration state: INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
20260718_000014 (head)

[1;33m  ▶[0m  Final service status:
NAME            STATUS                    PORTS
madar-api-1     Up 12 seconds             0.0.0.0:8000->8000/tcp, [::]:8000->8000/tcp
madar-db-1      Up 23 seconds (healthy)   0.0.0.0:5432->5432/tcp, [::]:5432->5432/tcp
madar-redis-1   Up 23 seconds (healthy)   0.0.0.0:6379->6379/tcp, [::]:6379->6379/tcp
madar-web-1     Up 12 seconds             0.0.0.0:3000->3000/tcp, [::]:3000->3000/tcp

[0;32m  ✓[0m  API health: {"status":"healthy"}
[0;32m  ✓[0m  Web status: HTTP 200

[0;32m========================================================
  ✓  CLEAN START COMPLETE
  All 4 services are running and healthy.
  Migrations applied to head.
========================================================[0m

__DURATION_SECONDS__=30.276
```

### Generated Artifacts
```text
evidence/rc_logs/01.log
evidence/rc_logs/01.meta
```

## Verification 02

### Status
Executed

### Exact Command Executed
```bash
bash verify/02_run_tests.sh
```

### Execution Duration
```text
START=2026-07-18T19:50:57+00:00
END=2026-07-18T19:51:09+00:00
DURATION_SECONDS=12.856
```

### Command Output
```text

========================================================
  MADAR — Automated Test Suite
  2026-07-18T19:50:57+00:00
========================================================
[1;33m  ▶[0m  Locating Python environment...
[0;32m  ✓[0m  Found virtual environment at /workspaces/MADAR/apps/api/.venv
[1;33m  ▶[0m  Checking API is healthy before running tests...
[0;32m  ✓[0m  API is healthy
[1;33m  ▶[0m  Running pytest from /workspaces/MADAR/apps/api...

============================= test session starts ==============================
platform linux -- Python 3.12.1, pytest-8.3.3, pluggy-1.6.0 -- /workspaces/MADAR/apps/api/.venv/bin/python3
cachedir: .pytest_cache
rootdir: /workspaces/MADAR/apps/api
configfile: pytest.ini
plugins: anyio-4.14.2
collecting ... collected 50 items

tests/test_assets_phase10.py::test_fixed_assets_route_is_accessible PASSED [  2%]
tests/test_assets_phase10.py::test_asset_assignments_route_is_accessible PASSED [  4%]
tests/test_auth.py::test_health_endpoint PASSED                          [  6%]
tests/test_auth.py::test_login_requires_credentials PASSED               [  8%]
tests/test_authorization.py::test_missing_token_is_rejected PASSED       [ 10%]
tests/test_business_foundation.py::test_cost_centers_route_is_accessible PASSED [ 12%]
tests/test_business_foundation.py::test_customer_groups_route_is_accessible PASSED [ 14%]
tests/test_business_foundation.py::test_brands_route_is_accessible PASSED [ 16%]
tests/test_crm_phase4.py::test_leads_list_is_accessible PASSED           [ 18%]
tests/test_crm_phase4.py::test_leads_create_and_update_status PASSED     [ 20%]
tests/test_crm_phase4.py::test_leads_filter_by_status PASSED             [ 22%]
tests/test_crm_phase4.py::test_pipelines_create_and_list PASSED          [ 24%]
tests/test_crm_phase4.py::test_stages_create_and_list PASSED             [ 26%]
tests/test_crm_phase4.py::test_opportunities_create_and_move_stage PASSED [ 28%]
tests/test_crm_phase4.py::test_activities_create_and_complete PASSED     [ 30%]
tests/test_crm_phase4.py::test_notes_create_and_retrieve_by_lead PASSED  [ 32%]
tests/test_finance_phase8.py::test_chart_of_accounts_route_is_accessible PASSED [ 34%]
tests/test_finance_phase8.py::test_journal_entries_route_is_accessible PASSED [ 36%]
tests/test_hr_phase9.py::test_employees_route_is_accessible PASSED       [ 38%]
tests/test_hr_phase9.py::test_attendance_route_is_accessible PASSED      [ 40%]
tests/test_hr_phase9.py::test_payroll_route_is_accessible PASSED         [ 42%]
tests/test_inventory_phase7.py::test_stock_movements_route_is_accessible PASSED [ 44%]
tests/test_inventory_phase7.py::test_stock_transfers_route_is_accessible PASSED [ 46%]
tests/test_inventory_phase7.py::test_stock_adjustments_route_is_accessible PASSED [ 48%]
tests/test_procurement_phase6.py::test_purchase_orders_route_is_accessible PASSED [ 50%]
tests/test_procurement_phase6.py::test_goods_receipts_route_is_accessible PASSED [ 52%]
tests/test_procurement_phase6.py::test_purchase_returns_route_is_accessible PASSED [ 54%]
tests/test_release_v01.py::test_health_endpoint PASSED                   [ 56%]
tests/test_release_v01.py::test_root_endpoint PASSED                     [ 58%]
tests/test_release_v01.py::test_company_registration PASSED              [ 60%]
tests/test_release_v01.py::test_duplicate_slug_rejected PASSED           [ 62%]
tests/test_release_v01.py::test_login_returns_tokens PASSED              [ 64%]
tests/test_release_v01.py::test_login_wrong_password_rejected PASSED     [ 66%]
tests/test_release_v01.py::test_me_endpoint PASSED                       [ 68%]
tests/test_release_v01.py::test_token_refresh PASSED                     [ 70%]
tests/test_release_v01.py::test_api_status_endpoint PASSED               [ 72%]
tests/test_release_v01.py::test_customers_full_crud PASSED               [ 74%]
tests/test_release_v01.py::test_suppliers_full_crud PASSED               [ 76%]
tests/test_release_v01.py::test_products_full_crud PASSED                [ 78%]
tests/test_release_v01.py::test_crm_leads_smoke PASSED                   [ 80%]
tests/test_release_v01.py::test_sales_quotations_smoke PASSED            [ 82%]
tests/test_release_v01.py::test_inventory_stock_movements_smoke PASSED   [ 84%]
tests/test_release_v01.py::test_finance_chart_of_accounts_smoke PASSED   [ 86%]
tests/test_release_v01.py::test_hr_employees_smoke PASSED                [ 88%]
tests/test_release_v01.py::test_assets_smoke PASSED                      [ 90%]
tests/test_release_v01.py::test_no_utcnow_deprecation_warning_in_crud_flows PASSED [ 92%]
tests/test_sales_phase5.py::test_quotations_route_is_accessible PASSED   [ 94%]
tests/test_sales_phase5.py::test_sales_orders_route_is_accessible PASSED [ 96%]
tests/test_sales_phase5.py::test_sales_invoices_route_is_accessible PASSED [ 98%]
tests/test_workflow_e2e.py::test_complete_12step_workflow PASSED         [100%]

============================= 50 passed in 11.93s ==============================

========================================================
  TEST RESULTS
========================================================
[0;32m  ✓[0m  Passed:   50 passed

[0;32m========================================================
  ✓  TEST SUITE PASSED — 50 passed
========================================================[0m

__DURATION_SECONDS__=12.856
```

### Generated Artifacts
```text
evidence/rc_logs/02.log
evidence/rc_logs/02.meta
```

## Verification 03

### Status
Executed

### Exact Command Executed
```bash
bash verify/03_seed_demo.sh
```

### Execution Duration
```text
START=2026-07-18T19:51:09+00:00
END=2026-07-18T19:51:14+00:00
DURATION_SECONDS=4.159
```

### Command Output
```text

========================================================
  MADAR — Demo Data Seeding
  2026-07-18T19:51:10+00:00
========================================================
[1;33m  ▶[0m  Checking API health...
[0;32m  ✓[0m  API is healthy
[1;33m  ▶[0m  Copying beta_seed.py into API container...
[0;32m  ✓[0m  Script copied
[1;33m  ▶[0m  Running beta_seed.py...

=================================================================
  MADAR Closed Beta — Demo Database Seeding
=================================================================

▶  Company
   ✓ Created: Gulf Electronics & Trading Ltd (ID 26)

▶  Branches
   ✓ Head Office – Riyadh
   ✓ Eastern Province Branch
   ✓ Dubai Sales Office

▶  Permissions & Roles
   ✓ Role [admin] — 33 permissions
   ✓ Role [sales-manager] — 16 permissions
   ✓ Role [inventory-manager] — 12 permissions
   ✓ Role [accountant] — 11 permissions

▶  Demo User Accounts
   ✓ Mohammed Al-Rashidi             admin@gulf-trading.demo              [admin]
   ✓ Sara Al-Mansouri                sales@gulf-trading.demo              [sales-manager]
   ✓ Khalid Al-Otaibi                inventory@gulf-trading.demo          [inventory-manager]
   ✓ Fatima Al-Zahrawi               accountant@gulf-trading.demo         [accountant]

▶  Warehouses
   ✓ Main Warehouse – Riyadh
   ✓ Eastern Province Warehouse
   ✓ Dubai Transit Hub
   ✓ Riyadh Returns Warehouse

▶  Product Categories
   ✓ Consumer Electronics
   ✓ Networking Equipment
   ✓ Office Equipment
   ✓ Smart Home Devices
   ✓ Spare Parts

▶  Units of Measure
   ✓ Piece
   ✓ Box
   ✓ Carton
   ✓ Pallet
   ✓ Set
   ✓ Meter

▶  Products
   ✓ 15 products seeded

▶  Customers
   ✓ 8 customers seeded

▶  Suppliers
   ✓ 5 suppliers seeded

▶  Sales Quotations
   ✓ 6 quotations seeded

▶  Sales Orders
   ✓ 6 orders seeded

▶  Sales Invoices
   ✓ 3 invoices seeded

▶  Stock Movements
   ✓ 13 stock movements seeded

=================================================================
  ✅  BETA DEMO DATABASE READY
=================================================================

  Company:    Gulf Electronics & Trading Ltd
  Slug:       beta-gulf-trading
  Company ID: 26

  ┌──────────────────────────────────────────────────────────┐
  │              DEMO USER CREDENTIALS                       │
  ├────────────────────────┬─────────────────────────────────┤
  │ Email                  │ Password          │ Role        │
  ├────────────────────────┼───────────────────┼─────────────┤
  │ admin@gulf-trading.demo│ BetaAdmin2026!    │ Admin       │
  │ sales@gulf-trading.demo│ BetaSales2026!    │ Sales Mgr   │
  │ inv.@gulf-trading.demo │ BetaInventory2026!│ Inv. Mgr    │
  │ acct@gulf-trading.demo │ BetaAccount2026!  │ Accountant  │
  └────────────────────────┴───────────────────┴─────────────┘

  Data Summary:
    Branches:    3
    Warehouses:  4
    Customers:   8
    Suppliers:   5
    Products:    15
    Quotations:  6
    Orders:      6
    Invoices:    3

  Access:
    Frontend: http://localhost:3000
    API Docs: http://localhost:8000/docs

========================================================
  SEED VALIDATION
========================================================
[0;32m  ✓[0m  Company created/verified
[0;32m  ✓[0m  Branches seeded
[0;32m  ✓[0m  Warehouses seeded
[0;32m  ✓[0m  Roles created
[0;32m  ✓[0m  Sales Manager role
[0;32m  ✓[0m  Inventory Manager role
[0;32m  ✓[0m  Accountant role
[0;32m  ✓[0m  Admin user
[0;32m  ✓[0m  Sales Manager user
[0;32m  ✓[0m  Inventory Manager user
[0;32m  ✓[0m  Accountant user
[0;32m  ✓[0m  Customers seeded
[0;32m  ✓[0m  Suppliers seeded
[0;32m  ✓[0m  Products seeded
[0;32m  ✓[0m  Quotations seeded
[0;32m  ✓[0m  Orders seeded
[0;32m  ✓[0m  Invoices seeded
[1;33m  ▶[0m  Verifying seeded data via API...
[0;32m  ✓[0m  Admin login: OK
[0;32m  ✓[0m  Company ID: 26
[0;32m  ✓[0m  Branches: 3 records (expected ≥3)
[0;32m  ✓[0m  Warehouses: 4 records (expected ≥4)
[0;32m  ✓[0m  Customers: 8 records (expected ≥8)
[0;32m  ✓[0m  Suppliers: 5 records (expected ≥5)
[0;32m  ✓[0m  Products: 15 records (expected ≥15)
[0;32m  ✓[0m  Quotations: 6 records (expected ≥6)
[0;32m  ✓[0m  Orders: 6 records (expected ≥6)
[0;32m  ✓[0m  Invoices: 3 records (expected ≥3)
[0;32m  ✓[0m  Stock Movements: 13 records (expected ≥13)

[0;32m========================================================
  ✓  DEMO DATA SEEDING COMPLETE
  Company: Gulf Electronics & Trading Ltd
  Credentials:
    admin@gulf-trading.demo    / BetaAdmin2026!
    sales@gulf-trading.demo    / BetaSales2026!
    inventory@gulf-trading.demo/ BetaInventory2026!
    accountant@gulf-trading.demo/ BetaAccount2026!
========================================================[0m

__DURATION_SECONDS__=4.159
```

### Generated Artifacts
```text
evidence/rc_logs/03.log
evidence/rc_logs/03.meta
```

## Verification 04

### Status
Executed

### Exact Command Executed
```bash
bash verify/04_smoke_tests.sh
```

### Execution Duration
```text
START=2026-07-18T19:51:14+00:00
END=2026-07-18T19:51:17+00:00
DURATION_SECONDS=3.139
```

### Command Output
```text

========================================================
  MADAR — API Smoke Tests
  2026-07-18T19:51:14+00:00
========================================================

[1;33m[1m▶  Section 1: Health & Infrastructure[0m
[0;32m  PASS[0m  GET /health → status=healthy
[0;32m  PASS[0m  GET / → name=MADAR ERP API
[0;32m  PASS[0m  GET /health/live (200) → HTTP 200
[0;32m  PASS[0m  GET /health/ready (200) → HTTP 200
[0;32m  PASS[0m  GET /docs (200) → HTTP 200
[0;32m  PASS[0m  GET /metrics (200) → HTTP 200

[1;33m[1m▶  Section 2: Authentication[0m
[0;32m  PASS[0m  POST /auth/login [admin] → token issued
[0;32m  PASS[0m  POST /auth/login [wrong password] → 401 → HTTP 401
[0;32m  PASS[0m  POST /auth/login [Sales Manager] → token issued
[0;32m  PASS[0m  POST /auth/login [Inventory Manager] → token issued
[0;32m  PASS[0m  POST /auth/login [Accountant] → token issued
[0;32m  PASS[0m  POST /auth/refresh → 200 → HTTP 200
[0;32m  PASS[0m  GET /api/v1/me (no token) → 401 → HTTP 401
[0;32m  PASS[0m  GET /api/v1/me (with token) → 200 → HTTP 200

[1;33m[1m▶  Section 3: Master Data — Branches[0m
[0;32m  PASS[0m  GET /master-data/branches (≥3) → 3 records (≥3)
[0;32m  PASS[0m  POST /master-data/branches → created ID=29
[0;32m  PASS[0m  PUT /master-data/branches/29 → 200 → HTTP 200
[0;32m  PASS[0m  DELETE /master-data/branches/29 → 200 → HTTP 200
[0;32m  PASS[0m  POST /master-data/branches (empty body) → 422 → HTTP 422

[1;33m[1m▶  Section 4: Master Data — Customers[0m
[0;32m  PASS[0m  GET /master-data/customers (≥8) → 8 records (≥8)
[0;32m  PASS[0m  POST /master-data/customers → created ID=12
[0;32m  PASS[0m  DELETE /master-data/customers/12 → cleaned up
[0;32m  PASS[0m  POST /master-data/customers (empty body) → 422 → HTTP 422

[1;33m[1m▶  Section 5: Master Data — Products[0m
[0;32m  PASS[0m  GET /master-data/products (≥15) → 15 records (≥15)
[0;32m  PASS[0m  POST /master-data/products (empty body) → 422 → HTTP 422

[1;33m[1m▶  Section 6: Warehouses & Suppliers[0m
[0;32m  PASS[0m  GET /master-data/warehouses (≥4) → 4 records (≥4)
[0;32m  PASS[0m  GET /master-data/suppliers (≥5) → 5 records (≥5)

[1;33m[1m▶  Section 7: Sales Pipeline[0m
[0;32m  PASS[0m  GET /sales/quotations (≥6) → 6 records (≥6)
[0;32m  PASS[0m  GET /sales/orders (≥6) → 6 records (≥6)
[0;32m  PASS[0m  GET /sales/invoices (≥3) → 3 records (≥3)

[1;33m[1m▶  Section 8: Inventory[0m
[0;32m  PASS[0m  GET /inventory/stock-movements (≥13) → 13 records (≥13)

[1;33m[1m▶  Section 9: Dashboard[0m
[0;32m  PASS[0m  Dashboard KPI branches=3 (≥3)
[0;32m  PASS[0m  Dashboard KPI warehouses=4 (≥4)
[0;32m  PASS[0m  Dashboard KPI customers=8 (≥8)
[0;32m  PASS[0m  Dashboard KPI suppliers=5 (≥5)
[0;32m  PASS[0m  Dashboard KPI products=15 (≥15)
[0;32m  PASS[0m  Dashboard KPI quotations=6 (≥6)
[0;32m  PASS[0m  Dashboard KPI sales_orders=6 (≥6)
[0;32m  PASS[0m  Dashboard KPI sales_invoices=3 (≥3)

[1;33m[1m▶  Section 10: Security[0m
[0;32m  PASS[0m  GET /api/v1/me (no token) → 401 → HTTP 401
[0;32m  PASS[0m  POST /auth/login (unknown user) → 401 → HTTP 401
     NOTE: GET /api/v1/master-data/branches (no token) → HTTP 200
     KNOWN LIMITATION: Auth not enforced on resource GET routes (tracked: v1.1.0)

========================================================
  SMOKE TEST RESULTS
========================================================
[0;32m  PASSED: 56[0m

[0;32m========================================================
  ✓  ALL 56 SMOKE TESTS PASSED
========================================================[0m

__DURATION_SECONDS__=3.139
```

### Generated Artifacts
```text
evidence/rc_logs/04.log
evidence/rc_logs/04.meta
```

## Verification 05

### Status
Executed

### Exact Command Executed
```bash
bash verify/05_browser_workflow.sh
```

### Execution Duration
```text
START=2026-07-18T19:51:17+00:00
END=2026-07-18T19:51:19+00:00
DURATION_SECONDS=2.254
```

### Command Output
```text

========================================================
  MADAR — End-to-End Browser Workflow Verification
  2026-07-18T19:51:17+00:00
========================================================

[1;33m[1mStep 1: Pre-flight: API and Frontend are reachable[0m
[0;32m  ✓[0m  API: {"status":"healthy"}
[0;32m  ✓[0m  Frontend: HTTP 200

[1;33m[1mStep 2: Register new company (simulates registration page)[0m
[0;32m  ✓[0m  Company registered: ID=27, slug=wf-test-04277

[1;33m[1mStep 3: Login (simulates login page)[0m
[0;32m  ✓[0m  Login successful — JWT token issued
[0;32m  ✓[0m  Current user: WF Test Admin (company_id=27)

[1;33m[1mStep 4: View Dashboard (simulates dashboard page load)[0m
[0;32m  ✓[0m  Dashboard loaded — branches=1 (newly registered company)

[1;33m[1mStep 5: Create Branch (simulates Branches → Add Branch)[0m
[0;32m  ✓[0m  Branch created: ID=31

[1;33m[1mStep 6: Create Warehouse (simulates Warehouses → Add Warehouse)[0m
[0;32m  ✓[0m  Warehouse created: ID=6

[1;33m[1mStep 7: Create Customer (simulates Customers → Add Customer)[0m
[0;32m  ✓[0m  Customer created: ID=13

[1;33m[1mStep 8: Create Supplier (simulates Suppliers → Add Supplier)[0m
[0;32m  ✓[0m  Supplier created: ID=9

[1;33m[1mStep 9: Create Product (simulates Products → Add Product)[0m
     Using category_id=9, unit_of_measure_id=10
[0;32m  ✓[0m  Product created: ID=19

[1;33m[1mStep 10: Create Quotation (simulates Quotations → Create)[0m
[0;32m  ✓[0m  Quotation created: ID=8

[1;33m[1mStep 11: Create Sales Order (simulates Orders → Create)[0m
[0;32m  ✓[0m  Sales Order created: ID=8

[1;33m[1mStep 12: Create Invoice (simulates Invoices → Create)[0m
[0;32m  ✓[0m  Invoice created: ID=5

[1;33m[1mStep 13: Record Stock Movement (simulates Inventory → New Movement)[0m
[0;32m  ✓[0m  Stock Movement created: ID=15

[1;33m[1mStep 14: Verify Dashboard KPIs reflect all created data[0m
[0;32m  ✓[0m  Dashboard.branches=2 (≥1)
[0;32m  ✓[0m  Dashboard.warehouses=1 (≥1)
[0;32m  ✓[0m  Dashboard.customers=1 (≥1)
[0;32m  ✓[0m  Dashboard.suppliers=1 (≥1)
[0;32m  ✓[0m  Dashboard.products=1 (≥1)
[0;32m  ✓[0m  Dashboard.quotations=1 (≥1)
[0;32m  ✓[0m  Dashboard.sales_orders=1 (≥1)
[0;32m  ✓[0m  Dashboard.sales_invoices=1 (≥1)

[1;33m[1mStep 15: Verify frontend routes serve HTTP 200[0m
[0;32m  ✓[0m  GET http://localhost:3000/ → HTTP 200
[0;32m  ✓[0m  GET http://localhost:3000/login → HTTP 200
[0;32m  ✓[0m  GET http://localhost:3000/register → HTTP 200
[0;32m  ✓[0m  GET http://localhost:3000/dashboard → HTTP 200
[0;32m  ✓[0m  GET http://localhost:3000/branches → HTTP 200
[0;32m  ✓[0m  GET http://localhost:3000/warehouses → HTTP 200
[0;32m  ✓[0m  GET http://localhost:3000/customers → HTTP 200
[0;32m  ✓[0m  GET http://localhost:3000/suppliers → HTTP 200
[0;32m  ✓[0m  GET http://localhost:3000/products → HTTP 200
[0;32m  ✓[0m  GET http://localhost:3000/quotations → HTTP 200
[0;32m  ✓[0m  GET http://localhost:3000/orders → HTTP 200
[0;32m  ✓[0m  GET http://localhost:3000/invoices → HTTP 200
[0;32m  ✓[0m  GET http://localhost:3000/profile → HTTP 200

========================================================
  WORKFLOW VERIFICATION RESULTS
========================================================

  Company registered: wf-test-04277 (ID 27)
  Resources created:
    Branch ID:     31
    Warehouse ID:  6
    Customer ID:   13
    Supplier ID:   9
    Product ID:    19
    Quotation ID:  8
    Order ID:      8
    Invoice ID:    5
    Movement ID:   15

[0;32m  PASSED: 36[0m

[0;32m========================================================
  ✓  END-TO-END WORKFLOW COMPLETE
  All 15 steps executed successfully.
  36 assertions passed, 0 failed.
========================================================[0m

__DURATION_SECONDS__=2.254
```

### Generated Artifacts
```text
evidence/rc_logs/05.log
evidence/rc_logs/05.meta
```

## Verification 06

### Status
Executed

### Exact Command Executed
```bash
/home/codespace/.python/current/bin/python -m pytest apps/api/tests/test_release_v01.py -q
```

### Execution Duration
```text
START=2026-07-18T19:51:19+00:00
END=2026-07-18T19:51:19+00:00
DURATION_SECONDS=0.299
```

### Command Output
```text
/home/codespace/.python/current/bin/python: No module named pytest
__DURATION_SECONDS__=0.299
```

### Generated Artifacts
```text
evidence/rc_logs/06.log
evidence/rc_logs/06.meta
```

