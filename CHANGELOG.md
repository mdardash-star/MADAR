# MADAR ERP SaaS — Changelog

All notable changes are documented here, ordered newest-first.  
Format: `## [version] — YYYY-MM-DD`  
Types: **Added** | **Fixed** | **Changed** | **Removed** | **Security**

---

## [0.1.0] — 2026-07-18 🎉 Release v0.1

### Release verification
- **48 backend tests passing, 0 failed**
- Alembic migration head: `20260718_000014`
- Frontend: 9 static pages, Next.js production build clean
- Docker Compose: 4 services (db, redis, api, web) healthy
- See [RELEASE_NOTES_v0.1.md](RELEASE_NOTES_v0.1.md) for full details

### Added
- `tests/test_release_v01.py` — 18 release-gate acceptance tests covering health, company registration, login, JWT refresh, customer/supplier/product CRUD, and cross-module smoke tests.
- `RELEASE_NOTES_v0.1.md` — Full release notes with verification evidence.
- `INSTALL.md` — Complete installation guide (Docker Compose + local dev + production checklist).
- `QUICK_START.md` — 5-minute getting-started guide with curl examples.
- Alembic migration `20260718_000014_products_brand_audit_tenants` — adds `brand_id` (FK to `brands`) and `image_url` columns to `products`; creates `tenants` and `audit_logs` tables that were missing from the migration chain.

### Fixed
- Schema drift: `products` table was missing `brand_id` and `image_url` columns that the ORM model declared.
- Schema drift: `audit_logs` and `tenants` ORM models had no corresponding database tables.

---

## [0.11.0] — 2026-07-18

### Added
- **Phase 4 — CRM Module**: Full Customer Relationship Management backend.
  - ORM models: `CrmLead`, `CrmPipeline`, `CrmStage`, `CrmOpportunity`, `CrmActivity`, `CrmNote`.
  - Alembic migration `20260718_000010_crm_schema` (6 tables with all indexes).
  - `CRMService` with full CRUD for all 6 entities including soft-delete and filtered list queries.
  - `/api/v1/crm` route module (leads, pipelines, stages, opportunities, activities, notes).
  - `tests/test_crm_phase4.py` — 8 acceptance tests covering PH4-001 through PH4-005; all pass.
- Alembic migration `20260718_000011_companies_timestamps` — adds `created_at`, `updated_at`, `is_deleted`, `deleted_at` to `companies` and `branches` tables.
- Alembic migration `20260718_000012_identity_timestamps` — adds audit columns to `roles`, `permissions`, `users`.
- Alembic migration `20260718_000013_fix_roles_slug_uniqueness` — changes global unique slug index to per-company `(company_id, slug)` composite unique index.
- Planning documents: `PRODUCT_ROADMAP.md`, `PRODUCT_BACKLOG.md`, `MILESTONES.md`, `CHANGELOG.md`.

### Fixed
- `app/core/security.py` — replaced `passlib` bcrypt context (incompatible with bcrypt ≥ 4.x) with direct `bcrypt` library calls for `get_password_hash` and `verify_password`.
- `app/models/role.py` — removed column-level `unique=True` on `slug`; uniqueness is now enforced at the per-company level via the composite index.

---

## [0.10.1] — 2026-07-18

### Fixed
- Added missing Alembic migration revision `20260718_000009_business_foundation_schema` to create all business-foundation tables (`brands`, `cost_centers`, `customer_groups`, `customer_contacts`, `customer_addresses`, `supplier_contacts`, `supplier_addresses`, `storage_locations`, `stock_opening_balances`, `barcodes`, `product_images`) that existed as ORM models but were absent from the migration chain.
- Release regression: 3 failing business-foundation smoke tests (`test_cost_centers_route_is_accessible`, `test_customer_groups_route_is_accessible`, `test_brands_route_is_accessible`) now pass.

### Added
- `RELEASE_AUDIT.md` — verified engineering audit report for the baseline handoff.
- `PRODUCT_ROADMAP.md` — 14-phase commercial ERP roadmap.
- `PRODUCT_BACKLOG.md` — 80 backlog items with priority, dependencies, effort, acceptance criteria, and test requirements.
- `MILESTONES.md` — 8 delivery milestones with exit criteria and timeline.
- `CHANGELOG.md` (this file).

---

## [0.10.0] — 2026-07-18

### Added
- **Phase 10 — Fixed Assets**: `fixed_assets` and `asset_assignments` ORM models, Alembic migration `20260718_000008_assets_schema`, `AssetsService`, `/api/v1/assets` route module, and 2 smoke tests.
- Router aggregation updated to include assets domain.

---

## [0.9.0] — 2026-07-18

### Added
- **Phase 9 — HR Foundation**: `employees`, `attendances`, `payrolls` ORM models, Alembic migration `20260718_000007_hr_schema`, `HRService`, `/api/v1/hr` route module.

---

## [0.8.0] — 2026-07-18

### Added
- **Phase 8 — Finance Foundation**: `chart_of_accounts`, `journal_entries`, `journal_entry_lines` ORM models, Alembic migration `20260718_000006_finance_schema`, `FinanceService`, `/api/v1/finance` route module.

---

## [0.7.0] — 2026-07-18

### Added
- **Phase 7 — Inventory Foundation**: `stock_movements`, `stock_transfers`, `stock_adjustments` ORM models, Alembic migration `20260718_000005_inventory_schema`, `InventoryService`, `/api/v1/inventory` route module.

---

## [0.6.0] — 2026-07-18

### Added
- **Phase 6 — Procurement Foundation**: `purchase_orders`, `goods_receipts`, `purchase_returns` ORM models, Alembic migration `20260718_000004_procurement_schema`, `ProcurementService`, `/api/v1/procurement` route module.

---

## [0.5.0] — 2026-07-18

### Added
- **Phase 5 — Sales Foundation**: `sales_quotations`, `sales_orders`, `sales_invoices` ORM models, Alembic migration `20260718_000003_sales_schema`, `SalesService`, `/api/v1/sales` route module.

---

## [0.4.0] — 2026-07-18

### Added
- **Phase 4 — Business Foundation**: extended CRM-adjacent entities: brands, cost centers, customer groups, customer/supplier contacts and addresses, storage locations, barcodes, product images, stock opening balances.
- `BusinessFoundationService` and `/api/v1/business-foundation` route module.
- Dashboard frontend page (`/dashboard`).
- Business foundation frontend page (`/business`).

---

## [0.3.0] — 2026-07-18

### Added
- **Phase 3 — Master Data**: departments, warehouses, customers, suppliers, product categories, units of measure, tax settings, currency settings, products, product variants.
- Alembic migration `20260718_000002_master_data_schema`.
- `MasterDataService` and `/api/v1/master-data` route module.
- Declarative SQLAlchemy base documented with docstring.

---

## [0.2.0] — 2026-07-18

### Added
- **Phase 2 — Identity & Security**: company registration, JWT login/refresh/me, RBAC roles and permissions, multi-tenant isolation.
- Models: `Company`, `Branch`, `Role`, `Permission`, `User`.
- Alembic migration `20260718_000001_initial_schema`.
- Auth routes (`/auth/login`, `/auth/refresh`, `/auth/me`), company routes.

---

## [0.1.0] — 2026-07-18

### Added
- **Phase 1 — Platform Foundation**: monorepo scaffold with `apps/api` (FastAPI) and `apps/web` (Next.js 14).
- Docker Compose: `db` (PostgreSQL), `redis`, `api`, `web`.
- GitHub Actions CI pipeline.
- Alembic scaffold + environment configuration.
- Ruff linter, pytest configuration, `.env.example` files.
- Next.js login and register pages with RTL Arabic layout.
- Health check endpoint `GET /health`.
