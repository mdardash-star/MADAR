# MADAR ERP SaaS — Product Backlog v1.0

> **Updated**: 2026-07-18  
> **Rules**: Never skip unfinished items. Close only after tests pass.

## Backlog item states
- `DONE` — implementation complete, tests passing, changelog updated
- `IN PROGRESS` — currently being implemented
- `TODO` — not yet started, ordered by priority

---

## PH1 — Platform Foundation

### PH1-001 Monorepo scaffold
- **Priority**: P0
- **Dependencies**: none
- **Effort**: 1 day
- **Status**: `DONE`
- **Acceptance criteria**: `apps/api` and `apps/web` directories exist with correct package structure; Docker Compose brings up all four services.
- **Tests**: `docker compose up --build` exits cleanly; `GET /health` returns 200.

### PH1-002 CI pipeline
- **Priority**: P0
- **Dependencies**: PH1-001
- **Effort**: 0.5 day
- **Status**: `DONE`
- **Acceptance criteria**: `.github/workflows/ci.yml` triggers on every push; backend + frontend build steps pass.
- **Tests**: GitHub Actions workflow completes without failures.

---

## PH2 — Identity & Security

### PH2-001 Company registration + admin bootstrap
- **Priority**: P0
- **Dependencies**: PH1-001
- **Effort**: 1 day
- **Status**: `DONE`
- **Acceptance criteria**: `POST /companies/register` creates company, branch, role, and first admin user atomically.
- **Tests**: Registration returns 201; duplicate slug returns 409.

### PH2-002 JWT auth (login / refresh / me)
- **Priority**: P0
- **Dependencies**: PH2-001
- **Effort**: 1 day
- **Status**: `DONE`
- **Acceptance criteria**: `POST /auth/login` returns `access_token` + `refresh_token`; `POST /auth/refresh` rotates tokens; `GET /auth/me` returns current user.
- **Tests**: Login with valid credentials returns tokens; invalid password returns 401; expired token returns 401.

### PH2-003 RBAC — roles, permissions, codenames
- **Priority**: P0
- **Dependencies**: PH2-002
- **Effort**: 1 day
- **Status**: `DONE`
- **Acceptance criteria**: Role model linked to permissions via association table; `require_permission` dependency enforces codename; missing permission returns 403.
- **Tests**: Route guarded with `require_permission("orders.view")` returns 403 without correct role.

### PH2-004 Multi-tenant isolation
- **Priority**: P0
- **Dependencies**: PH2-001
- **Effort**: 0.5 day
- **Status**: `DONE`
- **Acceptance criteria**: All queries filter by `company_id`; no row from tenant A is accessible in tenant B.
- **Tests**: Two separate company registrations; data from company A cannot be queried with company B token.

---

## PH3 — Master Data

### PH3-001 Departments, Warehouses CRUD
- **Priority**: P1
- **Dependencies**: PH2-001
- **Effort**: 0.5 day
- **Status**: `DONE`
- **Acceptance criteria**: Full CRUD with soft-delete; list supports pagination + search.
- **Tests**: Create, list, update, delete lifecycle passes; search filter returns only matching rows.

### PH3-002 Customers, Suppliers CRUD
- **Priority**: P1
- **Dependencies**: PH2-001
- **Effort**: 0.5 day
- **Status**: `DONE`
- **Acceptance criteria**: Same as PH3-001.
- **Tests**: Same as PH3-001.

### PH3-003 Product catalogue (categories, UoM, products, variants)
- **Priority**: P1
- **Dependencies**: PH3-002
- **Effort**: 1 day
- **Status**: `DONE`
- **Acceptance criteria**: Products link to category and UoM; variants link to products; SKU unique per company.
- **Tests**: Create product with variant; SKU uniqueness constraint prevents duplicate.

### PH3-004 Tax settings, Currency settings
- **Priority**: P1
- **Dependencies**: PH2-001
- **Effort**: 0.5 day
- **Status**: `DONE`
- **Acceptance criteria**: CRUD; rate_percent validated 0–100.
- **Tests**: Rate outside range returns 422.

### PH3-005 Business foundation entities
- **Priority**: P1
- **Dependencies**: PH3-002, PH3-003
- **Effort**: 1.5 days
- **Status**: `DONE`
- **Acceptance criteria**: Brands, cost centers, customer groups, customer/supplier contacts & addresses, storage locations, barcodes, product images, stock opening balances all present with CRUD + soft-delete.
- **Tests**: Route smoke tests return 200; migration `20260718_000009` creates all tables.

---

## PH4 — CRM

### PH4-001 CRM Leads
- **Priority**: P1
- **Dependencies**: PH3-002
- **Effort**: 1.5 days
- **Status**: `DONE`
- **Acceptance criteria**: Lead model with source, status (new/contacted/qualified/lost), assigned_to, contact details, notes. Full CRUD + list + search + pagination.
- **Tests**: Create lead; update status; list filtered by status; soft-delete.

### PH4-002 CRM Pipelines & Stages
- **Priority**: P1
- **Dependencies**: PH4-001
- **Effort**: 1 day
- **Status**: `DONE`
- **Acceptance criteria**: Pipeline model with ordered stages; each stage has a name, probability %, and is_won/is_lost flags.
- **Tests**: Create pipeline with 3 stages; reorder stages; soft-delete.

### PH4-003 CRM Opportunities
- **Priority**: P1
- **Dependencies**: PH4-001, PH4-002
- **Effort**: 2 days
- **Status**: `DONE`
- **Acceptance criteria**: Opportunity linked to lead, customer, pipeline stage; expected_value, expected_close_date; stage transitions logged.
- **Tests**: Create opportunity; move to next stage; compute weighted pipeline value.

### PH4-004 CRM Activities
- **Priority**: P1
- **Dependencies**: PH4-003
- **Effort**: 1.5 days
- **Status**: `DONE`
- **Acceptance criteria**: Activity types: call, meeting, email, task. Linked to lead or opportunity. Has due_date, outcome, assigned_to.
- **Tests**: Create activity linked to opportunity; complete activity; list upcoming activities by assigned_to.

### PH4-005 CRM Notes
- **Priority**: P2
- **Dependencies**: PH4-001
- **Effort**: 0.5 day
- **Status**: `DONE`
- **Acceptance criteria**: Notes linked to any CRM entity (lead, opportunity). Timestamps, author, content.
- **Tests**: Create note; retrieve notes for a lead.

### PH4-006 Frontend — CRM module pages
- **Priority**: P2
- **Dependencies**: PH4-003, PH4-004
- **Effort**: 3 days
- **Status**: `TODO`
- **Acceptance criteria**: Kanban pipeline view; lead list with filters; opportunity detail page; activity timeline.
- **Tests**: Next.js build passes; no TypeScript errors.

---

## PH5 — Sales

### PH5-001 Sales Quotations CRUD
- **Priority**: P1
- **Dependencies**: PH3-003
- **Effort**: 1 day
- **Status**: `DONE`
- **Acceptance criteria**: Quotation with lines, discount, tax; status: draft/sent/accepted/rejected.
- **Tests**: Create quotation; list by company; soft-delete.

### PH5-002 Sales Orders CRUD
- **Priority**: P1
- **Dependencies**: PH5-001
- **Effort**: 1 day
- **Status**: `DONE`
- **Acceptance criteria**: Order with lines, customer, shipping address; status: confirmed/partial/delivered/cancelled.
- **Tests**: Create order; update status.

### PH5-003 Sales Invoices CRUD
- **Priority**: P1
- **Dependencies**: PH5-002
- **Effort**: 1 day
- **Status**: `DONE`
- **Acceptance criteria**: Invoice with amount_due, amount_paid, due_date; status: draft/sent/paid/overdue.
- **Tests**: Create invoice; mark as paid.

### PH5-004 Quotation → Order conversion
- **Priority**: P1
- **Dependencies**: PH5-001, PH5-002
- **Effort**: 0.5 day
- **Status**: `TODO`
- **Acceptance criteria**: `POST /sales/quotations/{id}/convert-to-order` creates a linked sales order and marks quotation as accepted.
- **Tests**: Conversion returns 201; second conversion returns 409.

### PH5-005 Order → Invoice conversion
- **Priority**: P1
- **Dependencies**: PH5-002, PH5-003
- **Effort**: 0.5 day
- **Status**: `TODO`
- **Acceptance criteria**: `POST /sales/orders/{id}/convert-to-invoice` creates invoice linked to order.
- **Tests**: Invoice created with correct totals; order status updated to invoiced.

### PH5-006 Sales Returns
- **Priority**: P2
- **Dependencies**: PH5-002
- **Effort**: 1 day
- **Status**: `TODO`
- **Acceptance criteria**: Return linked to original order; credit note generated; inventory restocked.
- **Tests**: Return creates credit note; product quantity increases in source warehouse.

### PH5-007 Payment Receipts
- **Priority**: P2
- **Dependencies**: PH5-003
- **Effort**: 1 day
- **Status**: `TODO`
- **Acceptance criteria**: Receipt linked to invoice; amount_received; payment_method; outstanding balance updated.
- **Tests**: Partial payment; full payment marks invoice as paid.

### PH5-008 Frontend — Sales module pages
- **Priority**: P2
- **Dependencies**: PH5-003
- **Effort**: 2 days
- **Status**: `TODO`
- **Acceptance criteria**: List/detail/create pages for quotations, orders, invoices. RTL Arabic support.
- **Tests**: Next.js build passes.

---

## PH6 — Purchasing

### PH6-001 Purchase Orders CRUD
- **Priority**: P1
- **Dependencies**: PH3-002
- **Effort**: 1 day
- **Status**: `DONE`
- **Acceptance criteria**: PO with lines, supplier, expected delivery date; status: draft/confirmed/received.
- **Tests**: Create PO; confirm PO.

### PH6-002 Goods Receipts CRUD
- **Priority**: P1
- **Dependencies**: PH6-001
- **Effort**: 1 day
- **Status**: `DONE`
- **Acceptance criteria**: GR linked to PO; received_qty per line; triggers stock movement.
- **Tests**: GR creates positive stock movement.

### PH6-003 Purchase Returns CRUD
- **Priority**: P1
- **Dependencies**: PH6-002
- **Effort**: 0.5 day
- **Status**: `DONE`
- **Acceptance criteria**: Return linked to GR; triggers negative stock movement.
- **Tests**: Return creates negative stock movement.

### PH6-004 Supplier Invoices
- **Priority**: P2
- **Dependencies**: PH6-001
- **Effort**: 1 day
- **Status**: `TODO`
- **Acceptance criteria**: Supplier invoice linked to PO; amount, due_date, payment_status.
- **Tests**: Create supplier invoice; mark as paid.

### PH6-005 Purchase Approval Workflow
- **Priority**: P2
- **Dependencies**: PH6-001
- **Effort**: 1.5 days
- **Status**: `TODO`
- **Acceptance criteria**: PO above threshold requires manager approval; approval/rejection tracked with approver, timestamp, comment.
- **Tests**: PO requires approval; approval changes status to confirmed; rejection changes to rejected.

### PH6-006 Frontend — Purchasing module pages
- **Priority**: P2
- **Dependencies**: PH6-002
- **Effort**: 2 days
- **Status**: `TODO`
- **Acceptance criteria**: List/detail/create pages for POs and GRs.
- **Tests**: Next.js build passes.

---

## PH7 — Inventory

### PH7-001 Stock Movements
- **Priority**: P1
- **Dependencies**: PH3-003
- **Effort**: 1 day
- **Status**: `DONE`
- **Acceptance criteria**: Every stock change recorded as signed movement with source reference.
- **Tests**: Create movement; stock balance updated.

### PH7-002 Stock Transfers + Adjustments
- **Priority**: P1
- **Dependencies**: PH7-001
- **Effort**: 1 day
- **Status**: `DONE`
- **Acceptance criteria**: Transfer between warehouses; adjustment for gains/losses.
- **Tests**: Transfer reduces source, increases destination.

### PH7-003 Inventory Valuation (FIFO/AVCO)
- **Priority**: P2
- **Dependencies**: PH7-001
- **Effort**: 2 days
- **Status**: `TODO`
- **Acceptance criteria**: Endpoint returns current valuation per product per warehouse using FIFO or AVCO method.
- **Tests**: FIFO and AVCO results verified with known data set.

### PH7-004 Physical / Cycle Count
- **Priority**: P2
- **Dependencies**: PH7-001
- **Effort**: 1.5 days
- **Status**: `TODO`
- **Acceptance criteria**: Count session created; actual quantities entered; variance adjustment generated automatically.
- **Tests**: Variance quantity creates adjustment movement.

### PH7-005 Lot & Serial Number Tracking
- **Priority**: P2
- **Dependencies**: PH7-001
- **Effort**: 2 days
- **Status**: `TODO`
- **Acceptance criteria**: Products flagged as lot/serial tracked; movements carry lot/serial number; traceability report available.
- **Tests**: Stock movement with lot; GR assigns lot numbers; return traced back to lot.

### PH7-006 Frontend — Inventory module pages
- **Priority**: P2
- **Dependencies**: PH7-002
- **Effort**: 2 days
- **Status**: `TODO`
- **Acceptance criteria**: Stock levels view; movement log; transfer form.
- **Tests**: Next.js build passes.

---

## PH8 — Accounting

### PH8-001 Chart of Accounts CRUD
- **Priority**: P1
- **Dependencies**: PH2-001
- **Effort**: 1 day
- **Status**: `DONE`
- **Acceptance criteria**: Hierarchical accounts (parent_id); account type (asset, liability, equity, revenue, expense); code unique per company.
- **Tests**: Create account; attach child account; soft-delete.

### PH8-002 Journal Entries CRUD
- **Priority**: P1
- **Dependencies**: PH8-001
- **Effort**: 1 day
- **Status**: `DONE`
- **Acceptance criteria**: Double-entry validation (debits == credits); entry date; reference; lines with account, debit, credit.
- **Tests**: Unbalanced entry returns 422; balanced entry persists.

### PH8-003 AR/AP Aging
- **Priority**: P2
- **Dependencies**: PH5-003, PH6-004
- **Effort**: 1.5 days
- **Status**: `TODO`
- **Acceptance criteria**: Aging report buckets: current, 1-30, 31-60, 61-90, 90+ days.
- **Tests**: Invoice created 45 days ago appears in 31-60 bucket.

### PH8-004 Trial Balance / P&L / Balance Sheet
- **Priority**: P2
- **Dependencies**: PH8-002
- **Effort**: 2 days
- **Status**: `TODO`
- **Acceptance criteria**: Trial balance sums debits and credits per account; P&L nets revenue minus expenses; balance sheet verifies assets = liabilities + equity.
- **Tests**: Known journal entries produce expected P&L figures.

### PH8-005 Bank Reconciliation
- **Priority**: P2
- **Dependencies**: PH8-002
- **Effort**: 2 days
- **Status**: `TODO`
- **Acceptance criteria**: Bank statement import (CSV); automatic matching with journal entries; unmatched items flagged.
- **Tests**: Import statement; auto-match; manual match of remaining items.

### PH8-006 Budget Management
- **Priority**: P3
- **Dependencies**: PH8-001
- **Effort**: 2 days
- **Status**: `TODO`
- **Acceptance criteria**: Budget lines per account per period; actual vs budget variance computed.
- **Tests**: Budget created; actual spending recorded; variance report is accurate.

### PH8-007 Frontend — Accounting module pages
- **Priority**: P2
- **Dependencies**: PH8-002
- **Effort**: 2 days
- **Status**: `TODO`
- **Acceptance criteria**: Chart of accounts tree view; journal entry form; P&L display.
- **Tests**: Next.js build passes.

---

## PH9 — HR & Payroll

### PH9-001 Employees CRUD
- **Priority**: P1
- **Dependencies**: PH3-001
- **Effort**: 1 day
- **Status**: `DONE`
- **Acceptance criteria**: Employee linked to department, branch; employment date; job title; basic salary.
- **Tests**: Create employee; update; soft-delete.

### PH9-002 Attendance Records
- **Priority**: P1
- **Dependencies**: PH9-001
- **Effort**: 0.5 day
- **Status**: `DONE`
- **Acceptance criteria**: Daily clock-in/clock-out records; late/absent flags.
- **Tests**: Create attendance; list by employee and date range.

### PH9-003 Payroll Records
- **Priority**: P1
- **Dependencies**: PH9-002
- **Effort**: 1 day
- **Status**: `DONE`
- **Acceptance criteria**: Payroll record per employee per period; gross, deductions, net computed.
- **Tests**: Create payroll record; verify net = gross - deductions.

### PH9-004 Leave Management
- **Priority**: P2
- **Dependencies**: PH9-001
- **Effort**: 1.5 days
- **Status**: `TODO`
- **Acceptance criteria**: Leave types (annual, sick, unpaid); request / approval workflow; balance tracking.
- **Tests**: Request leave; approve; balance deducted; second request above balance rejected.

### PH9-005 Payroll Run Automation
- **Priority**: P2
- **Dependencies**: PH9-003, PH9-004
- **Effort**: 2 days
- **Status**: `TODO`
- **Acceptance criteria**: `POST /hr/payroll-runs` generates payroll for all active employees in a period; salary + allowances - deductions; locks period.
- **Tests**: Run payroll; verify total = sum of individual payrolls; rerun returns 409.

### PH9-006 Payslip generation
- **Priority**: P2
- **Dependencies**: PH9-005
- **Effort**: 1 day
- **Status**: `TODO`
- **Acceptance criteria**: PDF payslip per employee per period downloadable via API.
- **Tests**: Request payslip; response is a valid PDF.

### PH9-007 Frontend — HR module pages
- **Priority**: P2
- **Dependencies**: PH9-003
- **Effort**: 2 days
- **Status**: `TODO`
- **Acceptance criteria**: Employee list; attendance calendar; payroll summary.
- **Tests**: Next.js build passes.

---

## PH10 — Projects & Assets

### PH10-001 Fixed Assets CRUD
- **Priority**: P1
- **Dependencies**: PH3-001
- **Effort**: 1 day
- **Status**: `DONE`
- **Acceptance criteria**: Asset with name, acquisition date, cost, useful life, depreciation method.
- **Tests**: Create asset; list; soft-delete.

### PH10-002 Asset Assignments
- **Priority**: P1
- **Dependencies**: PH10-001
- **Effort**: 0.5 day
- **Status**: `DONE`
- **Acceptance criteria**: Assign asset to employee or department; assignment history.
- **Tests**: Assign asset; reassign; history preserved.

### PH10-003 Asset Depreciation
- **Priority**: P2
- **Dependencies**: PH10-001
- **Effort**: 1.5 days
- **Status**: `TODO`
- **Acceptance criteria**: `POST /assets/{id}/depreciate` creates a journal entry for the depreciation amount using straight-line or declining-balance method.
- **Tests**: Depreciation amount correct per method; journal entry balanced.

### PH10-004 Asset Disposal
- **Priority**: P2
- **Dependencies**: PH10-003
- **Effort**: 1 day
- **Status**: `TODO`
- **Acceptance criteria**: Disposal records sale/scrap date and proceeds; gain/loss journal entry generated; asset status set to disposed.
- **Tests**: Dispose asset; verify journal entry; asset not returned in active list.

### PH10-005 Project Management — Projects & Tasks
- **Priority**: P1
- **Dependencies**: PH9-001
- **Effort**: 2 days
- **Status**: `TODO`
- **Acceptance criteria**: Project with name, start/end dates, manager, status. Tasks with assigned_to, due_date, priority, status.
- **Tests**: Create project; add task; complete task; project progress computed.

### PH10-006 Project Milestones & Resource Allocation
- **Priority**: P2
- **Dependencies**: PH10-005
- **Effort**: 1.5 days
- **Status**: `TODO`
- **Acceptance criteria**: Milestone linked to project with target date; resource (employee) linked to project with allocation %.
- **Tests**: Create milestone; allocate resource; over-allocation (> 100%) returns warning.

### PH10-007 Project Time Tracking
- **Priority**: P2
- **Dependencies**: PH10-005
- **Effort**: 1 day
- **Status**: `TODO`
- **Acceptance criteria**: Time entry linked to task and employee; hours, date, description.
- **Tests**: Log time; total hours on task updated.

### PH10-008 Frontend — Projects & Assets pages
- **Priority**: P2
- **Dependencies**: PH10-005
- **Effort**: 2 days
- **Status**: `TODO`
- **Acceptance criteria**: Project kanban; asset register table.
- **Tests**: Next.js build passes.

---

## PH11 — Field Service & Maintenance

### PH11-001 Service Requests
- **Priority**: P2
- **Dependencies**: PH4-001
- **Effort**: 1.5 days
- **Status**: `TODO`
- **Acceptance criteria**: Request from customer; description, priority, asset linked; status: open/assigned/in_progress/resolved/closed.
- **Tests**: Create request; assign technician; resolve; close.

### PH11-002 Work Orders
- **Priority**: P2
- **Dependencies**: PH11-001
- **Effort**: 2 days
- **Status**: `TODO`
- **Acceptance criteria**: Work order linked to service request; scheduled_date; technician; parts used (consumes inventory).
- **Tests**: Create work order; complete with parts; inventory decremented.

### PH11-003 Preventive Maintenance Schedules
- **Priority**: P3
- **Dependencies**: PH10-001
- **Effort**: 1.5 days
- **Status**: `TODO`
- **Acceptance criteria**: Recurring schedule linked to asset; generates work order automatically on due date.
- **Tests**: Schedule triggers work order generation at correct interval.

### PH11-004 Frontend — Field Service pages
- **Priority**: P3
- **Dependencies**: PH11-002
- **Effort**: 2 days
- **Status**: `TODO`
- **Acceptance criteria**: Service request queue; work order detail.
- **Tests**: Next.js build passes.

---

## PH12 — Dashboards & Reports

### PH12-001 Executive KPI dashboard backend
- **Priority**: P2
- **Dependencies**: PH5-003, PH8-002, PH9-003
- **Effort**: 2 days
- **Status**: `TODO`
- **Acceptance criteria**: Single endpoint returns revenue_mtd, outstanding_ar, stock_value, payroll_cost_mtd, open_orders.
- **Tests**: Endpoint returns all KPIs; values match underlying data.

### PH12-002 Sales Analytics report
- **Priority**: P2
- **Dependencies**: PH12-001
- **Effort**: 1 day
- **Status**: `TODO`
- **Acceptance criteria**: Revenue by period, by customer, top products.
- **Tests**: Revenue grouping correct.

### PH12-003 Inventory Analytics report
- **Priority**: P2
- **Dependencies**: PH12-001
- **Effort**: 1 day
- **Status**: `TODO`
- **Acceptance criteria**: Stock levels per warehouse; top moving products; slow movers.
- **Tests**: Report reflects movements.

### PH12-004 Finance Analytics report
- **Priority**: P2
- **Dependencies**: PH8-004
- **Effort**: 1 day
- **Status**: `TODO`
- **Acceptance criteria**: P&L trend; cash position; expense breakdown by category.
- **Tests**: Values match chart of accounts balances.

### PH12-005 PDF / Excel export
- **Priority**: P3
- **Dependencies**: PH12-002, PH12-003, PH12-004
- **Effort**: 1.5 days
- **Status**: `TODO`
- **Acceptance criteria**: Any report endpoint accepts `?format=pdf` or `?format=xlsx` and returns appropriate file.
- **Tests**: PDF response is valid; XLSX opens in Excel.

### PH12-006 Frontend — Dashboards & Reports pages
- **Priority**: P2
- **Dependencies**: PH12-001
- **Effort**: 3 days
- **Status**: `TODO`
- **Acceptance criteria**: Executive dashboard with charts; report selector; export button.
- **Tests**: Next.js build passes; charts render.

---

## PH13 — Notifications & Integrations

### PH13-001 In-app notification center
- **Priority**: P2
- **Dependencies**: PH2-002
- **Effort**: 1.5 days
- **Status**: `TODO`
- **Acceptance criteria**: Notification model; `GET /notifications` returns unread; `POST /notifications/{id}/read` marks read; WebSocket push on new notification.
- **Tests**: Create notification; mark read; unread count decrements.

### PH13-002 Email notifications (SMTP)
- **Priority**: P2
- **Dependencies**: PH13-001
- **Effort**: 1 day
- **Status**: `TODO`
- **Acceptance criteria**: Background task sends email on: new invoice, order confirmed, leave approved. SMTP credentials from env.
- **Tests**: Test email task invoked with correct template; SMTP call mocked.

### PH13-003 Webhook outbound
- **Priority**: P3
- **Dependencies**: PH13-001
- **Effort**: 1.5 days
- **Status**: `TODO`
- **Acceptance criteria**: Webhook endpoint registry; configurable events; signed payload (HMAC); retry on failure.
- **Tests**: Webhook fires on invoice.created; signature validates.

### PH13-004 REST API public registry
- **Priority**: P3
- **Dependencies**: PH2-003
- **Effort**: 2 days
- **Status**: `TODO`
- **Acceptance criteria**: API key management for external integrations; rate limiting; usage logging.
- **Tests**: API key created; request authenticated; over-limit returns 429.

### PH13-005 Frontend — Notification center UI
- **Priority**: P2
- **Dependencies**: PH13-001
- **Effort**: 1 day
- **Status**: `TODO`
- **Acceptance criteria**: Bell icon in nav with unread badge; notification dropdown with mark-all-read.
- **Tests**: Next.js build passes.

---

## PH14 — AI Assistant

### PH14-001 Natural language ERP query
- **Priority**: P3
- **Dependencies**: PH12-001
- **Effort**: 3 days
- **Status**: `TODO`
- **Acceptance criteria**: `POST /ai/query` accepts freeform text; routes to appropriate report endpoint and returns structured answer.
- **Tests**: "What is my revenue this month?" returns correct figure.

### PH14-002 AI-powered invoice OCR extraction
- **Priority**: P3
- **Dependencies**: PH6-004
- **Effort**: 3 days
- **Status**: `TODO`
- **Acceptance criteria**: Upload invoice image; AI extracts supplier, date, total, line items; pre-fills supplier invoice form.
- **Tests**: Known invoice image returns correct extracted fields.

### PH14-003 Smart reorder / demand forecasting
- **Priority**: P3
- **Dependencies**: PH7-001, PH12-003
- **Effort**: 4 days
- **Status**: `TODO`
- **Acceptance criteria**: ML model (or rule-based heuristic) suggests reorder quantity per product based on historical movements.
- **Tests**: Product with 90 days history returns non-null reorder suggestion.

### PH14-004 Anomaly detection
- **Priority**: P3
- **Dependencies**: PH8-002
- **Effort**: 3 days
- **Status**: `TODO`
- **Acceptance criteria**: Flag journal entries and invoices that deviate from statistical norms (> 3σ).
- **Tests**: Injected outlier flagged; normal entries not flagged.

### PH14-005 Conversational AI assistant chat
- **Priority**: P3
- **Dependencies**: PH14-001
- **Effort**: 4 days
- **Status**: `TODO`
- **Acceptance criteria**: WebSocket-based chat; assistant has context of logged-in user's company data; responds in Arabic and English.
- **Tests**: Chat session established; reply within 5 seconds; response grounded in company data.

### PH14-006 Frontend — AI assistant chat panel
- **Priority**: P3
- **Dependencies**: PH14-005
- **Effort**: 2 days
- **Status**: `TODO`
- **Acceptance criteria**: Floating chat button; chat window with history; typing indicator; RTL Arabic support.
- **Tests**: Next.js build passes; WebSocket connects.

---

## Backlog summary

| Phase | Total items | Done | In Progress | TODO |
|-------|-------------|------|-------------|------|
| PH1 | 2 | 2 | 0 | 0 |
| PH2 | 4 | 4 | 0 | 0 |
| PH3 | 5 | 5 | 0 | 0 |
| PH4 | 6 | 5 | 0 | 1 |
| PH5 | 8 | 3 | 0 | 5 |
| PH6 | 6 | 3 | 0 | 3 |
| PH7 | 6 | 2 | 0 | 4 |
| PH8 | 7 | 2 | 0 | 5 |
| PH9 | 7 | 3 | 0 | 4 |
| PH10 | 8 | 2 | 0 | 6 |
| PH11 | 4 | 0 | 0 | 4 |
| PH12 | 6 | 0 | 0 | 6 |
| PH13 | 5 | 0 | 0 | 5 |
| PH14 | 6 | 0 | 0 | 6 |
| **Total** | **80** | **31** | **0** | **49** |

**Next item to implement**: `PH4-006 Frontend — CRM module pages` or `PH5-004 Quotation → Order conversion` (next highest priority with dependencies met)
