# MADAR Release Candidate Bug Log

Date: 2026-07-18
Branch: main
Scope: RC stabilization only (no new features)

## Summary

- Total bugs fixed in RC: 1
- Critical open: 0
- High open: 0
- Medium open: 0
- Low open: 0

---

## BUG-RC-001

- Title: Deprecated UTC timestamp API usage caused high warning volume and future runtime risk
- Severity (before fix): High
- Severity (after fix): Closed
- Type: Stabilization, compatibility, and minor performance hygiene

### Affected files

- apps/api/app/models/*.py (all model timestamp defaults/onupdate paths)
- apps/api/app/services/assets_service.py
- apps/api/app/services/business_foundation_service.py
- apps/api/app/services/crm_service.py
- apps/api/app/services/finance_service.py
- apps/api/app/services/hr_service.py
- apps/api/app/services/inventory_service.py
- apps/api/app/services/master_data_service.py
- apps/api/app/services/procurement_service.py
- apps/api/app/services/sales_service.py
- apps/api/tests/test_release_v01.py

### Root cause

The codebase relied on datetime.utcnow() for:

- SQLAlchemy default and onupdate callables in model timestamp columns.
- Soft-delete timestamp assignment in service delete flows.

In Python 3.12, datetime.utcnow() emits DeprecationWarning. This generated high warning noise during acceptance tests (259 warnings) and increased risk of future breakage when deprecations are enforced more strictly.

### Fix implemented

- Replaced all model timestamp callables:
  - default=datetime.utcnow -> default=lambda: datetime.now(timezone.utc)
  - onupdate=datetime.utcnow -> onupdate=lambda: datetime.now(timezone.utc)
- Replaced all service soft-delete assignments:
  - deleted_at = datetime.utcnow() -> deleted_at = datetime.now(timezone.utc)
- Removed dynamic datetime import usage in master data delete flows and switched to explicit imports.

### Automated tests added/updated

- Updated: apps/api/tests/test_release_v01.py
- Added test: test_no_utcnow_deprecation_warning_in_crud_flows
- What it validates:
  - Customer, supplier, and product create/delete flows execute without emitting DeprecationWarning messages containing utcnow.

### Validation evidence

- Before fix: 49 passed, 259 warnings.
- After fix: 50 passed, 0 warnings in verify automated suite output.
- Browser workflow: passed end-to-end after fix.

### Release impact

- No API contract changes.
- No schema migration required.
- No feature behavior changes.
- Reduced warning noise and improved runtime forward-compatibility.
