# MADAR ERP SaaS — Milestones

> **Updated**: 2026-07-18

---

## M1 — Verified Platform Baseline ✅
**Target**: 2026-07-18  
**Status**: Achieved

### Scope
All infrastructure, identity, and master data phases complete with a verified release baseline:
- Monorepo scaffold (FastAPI + Next.js)
- Docker Compose: db, redis, api, web
- JWT auth, RBAC, multi-tenant isolation
- Master data + business foundation entities
- 9 Alembic migration revisions
- 22 backend tests passing
- Next.js production build passing
- RELEASE_AUDIT.md committed

### Exit criteria ✅
- [x] `alembic upgrade head` exits clean
- [x] `pytest -q` → 22 passed, 0 failed
- [x] `npm run build` → compiled successfully
- [x] RELEASE_AUDIT.md committed to repository

---

## M2 — CRM & Sales Complete
**Target**: 2026-07-30  
**Status**: In progress

### Scope
Full CRM pipeline operational; sales order-to-cash cycle complete with conversions and payments.

### Backlog items
| Item | Status |
|------|--------|
| PH4-001 CRM Leads | TODO |
| PH4-002 CRM Pipelines & Stages | TODO |
| PH4-003 CRM Opportunities | TODO |
| PH4-004 CRM Activities | TODO |
| PH4-005 CRM Notes | TODO |
| PH5-004 Quotation → Order conversion | TODO |
| PH5-005 Order → Invoice conversion | TODO |
| PH5-006 Sales Returns | TODO |
| PH5-007 Payment Receipts | TODO |

### Exit criteria
- [ ] All items above closed (tests passing)
- [ ] `pytest -q` → all passing
- [ ] `npm run build` → passing
- [ ] CHANGELOG updated
- [ ] PRODUCT_ROADMAP.md Phase 4 and Phase 5 status updated

---

## M3 — Procurement, Inventory & Accounting Complete
**Target**: 2026-08-15  
**Status**: Not started

### Scope
Supplier invoices and approvals; inventory valuation, cycle counts, lot tracking; trial balance, P&L, bank reconciliation.

### Backlog items
| Item | Status |
|------|--------|
| PH6-004 Supplier Invoices | TODO |
| PH6-005 Purchase Approval Workflow | TODO |
| PH7-003 Inventory Valuation | TODO |
| PH7-004 Physical / Cycle Count | TODO |
| PH7-005 Lot & Serial Number Tracking | TODO |
| PH8-003 AR/AP Aging | TODO |
| PH8-004 Trial Balance / P&L / Balance Sheet | TODO |
| PH8-005 Bank Reconciliation | TODO |
| PH8-006 Budget Management | TODO |

### Exit criteria
- [ ] All items above closed (tests passing)
- [ ] `pytest -q` → all passing

---

## M4 — HR, Payroll & Projects Complete
**Target**: 2026-08-31  
**Status**: Not started

### Scope
Leave management and automated payroll runs; full project management with tasks, milestones and time tracking; asset depreciation and disposal.

### Backlog items
| Item | Status |
|------|--------|
| PH9-004 Leave Management | TODO |
| PH9-005 Payroll Run Automation | TODO |
| PH9-006 Payslip generation | TODO |
| PH10-003 Asset Depreciation | TODO |
| PH10-004 Asset Disposal | TODO |
| PH10-005 Project Management — Projects & Tasks | TODO |
| PH10-006 Project Milestones & Resource Allocation | TODO |
| PH10-007 Project Time Tracking | TODO |

### Exit criteria
- [ ] All items above closed (tests passing)
- [ ] `pytest -q` → all passing

---

## M5 — Field Service & Dashboards
**Target**: 2026-09-15  
**Status**: Not started

### Scope
Work orders, service requests, preventive maintenance; executive KPI dashboard and analytics reports.

### Backlog items
| Item | Status |
|------|--------|
| PH11-001 Service Requests | TODO |
| PH11-002 Work Orders | TODO |
| PH11-003 Preventive Maintenance Schedules | TODO |
| PH12-001 Executive KPI dashboard backend | TODO |
| PH12-002 Sales Analytics | TODO |
| PH12-003 Inventory Analytics | TODO |
| PH12-004 Finance Analytics | TODO |
| PH12-005 PDF/Excel export | TODO |

### Exit criteria
- [ ] All items above closed
- [ ] Dashboard endpoint returns valid KPIs

---

## M6 — Frontend Complete (All Modules)
**Target**: 2026-09-30  
**Status**: Not started

### Scope
All frontend module pages implemented for CRM, Sales, Purchasing, Inventory, Accounting, HR, Projects, Field Service, and Dashboards.

### Backlog items
| Item | Status |
|------|--------|
| PH4-006 Frontend CRM | TODO |
| PH5-008 Frontend Sales | TODO |
| PH6-006 Frontend Purchasing | TODO |
| PH7-006 Frontend Inventory | TODO |
| PH8-007 Frontend Accounting | TODO |
| PH9-007 Frontend HR | TODO |
| PH10-008 Frontend Projects & Assets | TODO |
| PH11-004 Frontend Field Service | TODO |
| PH12-006 Frontend Dashboards | TODO |
| PH13-005 Frontend Notifications | TODO |

### Exit criteria
- [ ] All items above closed
- [ ] `npm run build` → passing
- [ ] No TypeScript errors
- [ ] RTL Arabic layout verified on all pages

---

## M7 — Notifications, Integrations & AI Assistant
**Target**: 2026-10-15  
**Status**: Not started

### Scope
In-app notifications, email alerts, webhooks, public API keys; AI assistant for natural language queries and conversational interface.

### Backlog items
| Item | Status |
|------|--------|
| PH13-001 In-app notification center | TODO |
| PH13-002 Email notifications | TODO |
| PH13-003 Webhook outbound | TODO |
| PH13-004 REST API public registry | TODO |
| PH14-001 Natural language ERP query | TODO |
| PH14-002 AI-powered invoice OCR | TODO |
| PH14-003 Smart reorder / demand forecasting | TODO |
| PH14-004 Anomaly detection | TODO |
| PH14-005 Conversational AI assistant chat | TODO |
| PH14-006 Frontend AI assistant panel | TODO |

### Exit criteria
- [ ] All items above closed
- [ ] AI assistant responds in < 5 seconds
- [ ] Webhook signature verification passes

---

## M8 — MADAR ERP v1.0 General Availability
**Target**: 2026-10-31  
**Status**: Not started

### Scope
Production hardening, security review, performance benchmarks, documentation, and deployment guide.

### Checklist
- [ ] All 80 backlog items DONE
- [ ] 0 open P0/P1 bugs
- [ ] API rate limiting in place
- [ ] Secrets rotated; no credentials in code
- [ ] OWASP Top 10 review complete
- [ ] README updated with full deployment guide
- [ ] Semantic version tag `v1.0.0` created
- [ ] CHANGELOG finalized

---

## Milestone timeline

```
M1  ██████████████████████████  2026-07-18  ✅
M2  ████████████████████░░░░░░  2026-07-30
M3  █████████████░░░░░░░░░░░░░  2026-08-15
M4  ██████████░░░░░░░░░░░░░░░░  2026-08-31
M5  ████████░░░░░░░░░░░░░░░░░░  2026-09-15
M6  ██████░░░░░░░░░░░░░░░░░░░░  2026-09-30
M7  ████░░░░░░░░░░░░░░░░░░░░░░  2026-10-15
M8  ██░░░░░░░░░░░░░░░░░░░░░░░░  2026-10-31
```
