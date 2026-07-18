# MADAR ERP SaaS — Product Roadmap v1.0

> **Role**: Product Owner / Lead Architect / Engineering Manager  
> **Target release**: MADAR ERP v1.0 Commercial SaaS  
> **Updated**: 2026-07-18

---

## Progress legend

| Symbol | Meaning |
|--------|---------|
| ✅ | Phase complete — all backlog items closed, tests passing |
| 🔶 | Phase in progress — partial implementation exists |
| ⬜ | Phase not started |

---

## Phase 1 — Platform Foundation ✅

**Goal**: Production-ready monorepo scaffold, Docker Compose stack, CI pipeline, and project standards.

| Item | Status |
|------|--------|
| Monorepo layout (`apps/api`, `apps/web`) | ✅ |
| FastAPI app skeleton + CORS + health endpoint | ✅ |
| Next.js 14 + TypeScript + Tailwind CSS scaffold | ✅ |
| PostgreSQL + Alembic migration scaffold | ✅ |
| Redis service | ✅ |
| Docker Compose (db, redis, api, web) | ✅ |
| GitHub Actions CI pipeline | ✅ |
| Environment configuration via `.env` | ✅ |
| Declarative SQLAlchemy base + session | ✅ |
| Ruff linter + pytest configuration | ✅ |

---

## Phase 2 — Identity & Security ✅

**Goal**: JWT auth, company registration, RBAC, refresh tokens, password hashing, and multi-tenant isolation.

| Item | Status |
|------|--------|
| Company registration + first-admin bootstrap | ✅ |
| JWT access + refresh tokens (python-jose) | ✅ |
| Password hashing (passlib/bcrypt) | ✅ |
| Login / refresh / current-user endpoints | ✅ |
| Company, Branch, Role, Permission models | ✅ |
| User model with company/branch/role FKs | ✅ |
| RBAC dependency + permission codenames | ✅ |
| Multi-tenant query isolation by company_id | ✅ |

---

## Phase 3 — Master Data ✅

**Goal**: Foundational reference data entities required by every other module.

| Item | Status |
|------|--------|
| Departments CRUD | ✅ |
| Warehouses CRUD | ✅ |
| Customers CRUD | ✅ |
| Suppliers CRUD | ✅ |
| Product Categories CRUD | ✅ |
| Units of Measure CRUD | ✅ |
| Tax Settings CRUD | ✅ |
| Currency Settings CRUD | ✅ |
| Products CRUD | ✅ |
| Product Variants CRUD | ✅ |
| Business foundation entities (brands, cost centers, customer groups, contacts, addresses, storage locations, barcodes, product images, stock opening balances) | ✅ |

---

## Phase 4 — CRM 🔶

**Goal**: Full Customer Relationship Management pipeline — leads, opportunities, activities, pipelines, and customer 360 view.

| Item | Status |
|------|--------|
| Basic customer/supplier entities | ✅ |
| Customer groups, contacts, addresses | ✅ |
| **CRM Leads** (capture, qualification, assignment) | ✅ |
| **CRM Opportunities** (pipeline stages, probability, expected value) | ✅ |
| **CRM Activities** (calls, meetings, tasks, emails) | ✅ |
| **CRM Pipeline** configuration (stages, conversion) | ✅ |
| **CRM Notes** | ✅ |
| **Customer 360 view** (interactions history) | ⬜ |
| Frontend: CRM module pages | ⬜ |

---

## Phase 5 — Sales ✅ (foundation)

**Goal**: Full order-to-cash cycle — quotations, orders, invoices, returns, payment receipts.

| Item | Status |
|------|--------|
| Sales Quotations CRUD | ✅ |
| Sales Orders CRUD | ✅ |
| Sales Invoices CRUD | ✅ |
| **Quotation → Order conversion** | ⬜ |
| **Order → Invoice conversion** | ⬜ |
| **Sales Returns** | ⬜ |
| **Payment Receipts** | ⬜ |
| **Pricing Rules / Discounts** | ⬜ |
| Frontend: Sales module pages | ⬜ |

---

## Phase 6 — Purchasing ✅ (foundation)

**Goal**: Purchase-to-pay cycle — purchase orders, goods receipts, invoices, returns.

| Item | Status |
|------|--------|
| Purchase Orders CRUD | ✅ |
| Goods Receipts CRUD | ✅ |
| Purchase Returns CRUD | ✅ |
| **Supplier Invoices** | ⬜ |
| **Purchase Approval Workflow** | ⬜ |
| **Landed Costs** | ⬜ |
| Frontend: Purchasing module pages | ⬜ |

---

## Phase 7 — Inventory ✅ (foundation)

**Goal**: Real-time stock control — movements, transfers, adjustments, valuation, reorder.

| Item | Status |
|------|--------|
| Stock Movements | ✅ |
| Stock Transfers | ✅ |
| Stock Adjustments | ✅ |
| **Lot / Serial Number Tracking** | ⬜ |
| **Reorder Point Alerts** | ⬜ |
| **Inventory Valuation (FIFO/AVCO)** | ⬜ |
| **Physical Count / Cycle Count** | ⬜ |
| Frontend: Inventory module pages | ⬜ |

---

## Phase 8 — Accounting ✅ (foundation)

**Goal**: Double-entry bookkeeping, chart of accounts, journal entries, financial statements.

| Item | Status |
|------|--------|
| Chart of Accounts CRUD | ✅ |
| Journal Entries CRUD | ✅ |
| **Account Payable Aging** | ⬜ |
| **Account Receivable Aging** | ⬜ |
| **Bank Reconciliation** | ⬜ |
| **Trial Balance / P&L / Balance Sheet** | ⬜ |
| **Tax Reports (VAT)** | ⬜ |
| **Budget Management** | ⬜ |
| Frontend: Accounting module pages | ⬜ |

---

## Phase 9 — HR & Payroll ✅ (foundation)

**Goal**: Employee lifecycle, attendance, leave, and payroll processing.

| Item | Status |
|------|--------|
| Employees CRUD | ✅ |
| Attendance records | ✅ |
| Payroll records | ✅ |
| **Leave Management** | ⬜ |
| **Payroll Run automation** | ⬜ |
| **Payslip generation** | ⬜ |
| **Employee Onboarding Workflow** | ⬜ |
| Frontend: HR module pages | ⬜ |

---

## Phase 10 — Projects & Assets 🔶

**Goal**: Project tracking with tasks and milestones; fixed asset lifecycle and depreciation.

| Item | Status |
|------|--------|
| Fixed Assets CRUD | ✅ |
| Asset Assignments | ✅ |
| **Asset Depreciation (Straight-line / Declining)** | ⬜ |
| **Asset Disposal** | ⬜ |
| **Project management (projects, tasks, milestones)** | ⬜ |
| **Project resource allocation** | ⬜ |
| **Project time-tracking** | ⬜ |
| Frontend: Projects & Assets pages | ⬜ |

---

## Phase 11 — Field Service & Maintenance ⬜

**Goal**: Work orders, service requests, preventive maintenance schedules, technician dispatch.

| Item | Status |
|------|--------|
| Service Requests (customer-facing) | ⬜ |
| Work Orders (internal execution) | ⬜ |
| Maintenance Schedules (recurring jobs) | ⬜ |
| Technician Assignment & Dispatch | ⬜ |
| Parts & Material Consumption on Work Orders | ⬜ |
| Service Reports & Completion Sign-off | ⬜ |
| Frontend: Field Service module pages | ⬜ |

---

## Phase 12 — Dashboards & Reports ⬜

**Goal**: Cross-module analytics, KPI dashboards, configurable reports, and data exports.

| Item | Status |
|------|--------|
| Executive dashboard (KPIs) | ⬜ |
| Sales analytics (pipeline, revenue) | ⬜ |
| Inventory analytics (stock levels, movement) | ⬜ |
| Finance analytics (P&L, cash flow) | ⬜ |
| HR analytics (headcount, attendance) | ⬜ |
| Configurable report builder | ⬜ |
| PDF / Excel export | ⬜ |
| Frontend: Dashboard & Reports pages | ⬜ |

---

## Phase 13 — Notifications & Integrations ⬜

**Goal**: Real-time notifications, webhooks, email alerts, and third-party API integrations.

| Item | Status |
|------|--------|
| In-app notification center | ⬜ |
| Email notifications (SMTP/SendGrid) | ⬜ |
| Webhook outbound (event-driven) | ⬜ |
| WhatsApp / SMS alerts | ⬜ |
| REST API for external integrations | ⬜ |
| OAuth2 app registry (third-party) | ⬜ |
| Frontend: Notification center UI | ⬜ |

---

## Phase 14 — AI Assistant ⬜

**Goal**: Embedded AI co-pilot for smart search, business insights, auto-fill, and anomaly detection.

| Item | Status |
|------|--------|
| Natural language query for ERP data | ⬜ |
| AI-powered invoice data extraction (OCR) | ⬜ |
| Smart reorder / demand forecasting | ⬜ |
| Anomaly detection (fraud, errors) | ⬜ |
| Conversational assistant (chat widget) | ⬜ |
| Frontend: AI assistant chat panel | ⬜ |

---

## Overall progress

| Phase | Title | Status |
|-------|-------|--------|
| 1 | Platform Foundation | ✅ Complete |
| 2 | Identity & Security | ✅ Complete |
| 3 | Master Data | ✅ Complete |
| 4 | CRM | 🔶 Core backend complete, frontend pending |
| 5 | Sales | 🔶 Foundation done |
| 6 | Purchasing | 🔶 Foundation done |
| 7 | Inventory | 🔶 Foundation done |
| 8 | Accounting | 🔶 Foundation done |
| 9 | HR & Payroll | 🔶 Foundation done |
| 10 | Projects & Assets | 🔶 Assets done, Projects pending |
| 11 | Field Service & Maintenance | ⬜ Not started |
| 12 | Dashboards & Reports | ⬜ Not started |
| 13 | Notifications & Integrations | ⬜ Not started |
| 14 | AI Assistant | ⬜ Not started |
