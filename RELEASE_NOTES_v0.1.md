# MADAR ERP SaaS — Release Notes v0.1

**Release date**: 2026-07-18  
**Release type**: Foundation Release  
**Status**: General Availability

---

## Overview

MADAR v0.1 is the first production-ready foundation release of the MADAR ERP SaaS platform. It delivers a fully functional multi-tenant backend, a modern RTL-capable frontend, and a verified end-to-end stack that can be deployed from scratch using a single Docker Compose command.

---

## Release verification summary

| Requirement | Result |
|-------------|--------|
| Application starts from scratch | ✅ Pass |
| Docker Compose launches (db, redis, api, web) | ✅ Pass |
| Database migrations run (`alembic upgrade head`) | ✅ Pass — 14 revisions at head |
| Login returns JWT tokens | ✅ Pass |
| Company creation bootstraps admin user | ✅ Pass |
| Dashboard page loads | ✅ Pass — Next.js build compiles cleanly |
| Customers CRUD | ✅ Pass |
| Suppliers CRUD | ✅ Pass |
| Products CRUD | ✅ Pass |
| Automated tests | ✅ Pass — **48 passed, 0 failed** |

---

## What's included

### Platform (Phase 1 & 2)
- Monorepo: `apps/api` (FastAPI) + `apps/web` (Next.js 14)
- Docker Compose stack: PostgreSQL 16, Redis 7, API, Web
- GitHub Actions CI pipeline
- JWT authentication (login, refresh, `/auth/me`)
- Company registration with admin user bootstrap
- Multi-tenant isolation by `company_id`
- RBAC: roles, permissions, per-company role slug uniqueness
- bcrypt password hashing (compatible with bcrypt ≥ 4.x)

### Master Data (Phase 3)
- Departments, Warehouses
- Customers, Suppliers
- Product Categories, Units of Measure
- Tax Settings, Currency Settings
- Products (with brand, category, UoM links)
- Product Variants
- Full CRUD + soft-delete + pagination + search on all entities

### Business Foundation (Phase 4 foundation)
- Brands, Cost Centers, Customer Groups
- Customer and Supplier Contacts & Addresses
- Storage Locations, Barcodes, Product Images
- Stock Opening Balances

### CRM (Phase 4 — backend complete)
- Leads (create/qualify/assign/soft-delete)
- Pipelines and ordered Stages with win/loss probability
- Opportunities (pipeline stage tracking, expected value)
- Activities (call, meeting, email, task with due dates and outcomes)
- Notes linked to leads and opportunities

### Sales (Phase 5 — foundation)
- Sales Quotations, Sales Orders, Sales Invoices CRUD

### Purchasing (Phase 6 — foundation)
- Purchase Orders, Goods Receipts, Purchase Returns CRUD

### Inventory (Phase 7 — foundation)
- Stock Movements, Transfers, Adjustments

### Accounting (Phase 8 — foundation)
- Chart of Accounts, Journal Entries

### HR & Payroll (Phase 9 — foundation)
- Employees, Attendance Records, Payroll Records

### Fixed Assets (Phase 10 — foundation)
- Fixed Assets, Asset Assignments

### Database schema
- 14 Alembic migration revisions
- All ORM models fully synchronized with the database schema
- Zero schema drift (verified by automated scan)

### Frontend
- Next.js 14 + React 18 + TypeScript + Tailwind CSS
- Pages: `/`, `/login`, `/register`, `/dashboard`, `/business`, `/profile`
- RTL Arabic layout support
- Production build: 9 static pages, 87.2 KB shared JS

---

## API surface

- **156 REST endpoints** across 13 route modules
- Versioned under `/api/v1/`
- Interactive docs at `http://localhost:8000/docs`
- ReDoc at `http://localhost:8000/redoc`

---

## Fixes included in this release

| Issue | Fix |
|-------|-----|
| `passlib` incompatible with bcrypt ≥ 4.x | Replaced with direct `bcrypt` library calls |
| `roles.slug` unique constraint global (multi-tenant conflict) | Changed to per-company composite unique index `(company_id, slug)` |
| Missing `created_at`/`is_deleted` on `companies`, `branches`, `roles`, `permissions`, `users` | Migrations 11–12 added audit columns with backfill |
| `brand_id` and `image_url` missing from `products` table | Migration 14 added columns with FK to `brands` |
| `audit_logs` and `tenants` ORM models had no corresponding tables | Migration 14 created both tables |
| Business-foundation tables absent from migration chain | Migration 9 added 11 tables |

---

## Known limitations

| Area | Limitation |
|------|-----------|
| CRM | Frontend pages not yet implemented (PH4-006 backlog) |
| Sales | Quotation→Order, Order→Invoice conversions pending (PH5-004, PH5-005) |
| Accounting | P&L, Trial Balance, Bank Reconciliation pending |
| HR | Leave management, payroll run automation pending |
| Dashboards | No analytics or reports yet (Phase 12) |
| Notifications | Not yet implemented (Phase 13) |
| AI Assistant | Not yet implemented (Phase 14) |

---

## Upgrade notes

This is the first release. No upgrade path from a previous version is required.

For new installations, follow [INSTALL.md](INSTALL.md) or [QUICK_START.md](QUICK_START.md).

---

## Checksums

| Artifact | Value |
|----------|-------|
| Backend tests | 48 passed, 0 failed |
| Alembic head | `20260718_000014` |
| Frontend routes | 9 static pages |
| API endpoints | 156 |
| Alembic revisions | 14 |
