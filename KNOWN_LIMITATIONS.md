# MADAR v1.0.0-rc1 — Known Limitations

**Version**: v1.0.0-rc1  
**Date**: 2026-07-18  
**Status**: Release Candidate  

This document lists known limitations, deferred features, and technical debt present in the v1.0.0-rc1 release. Each item includes severity, impact, and planned resolution.

---

## Summary

| Category | Count |
|----------|-------|
| Infrastructure | 4 |
| API / Backend | 6 |
| Frontend | 5 |
| Security | 3 |
| Data / Database | 3 |
| Documentation | 2 |
| **Total** | **23** |

---

## Infrastructure Limitations

### INF-01 — Single-Instance Deployment Only
**Severity**: Medium  
**Impact**: No horizontal scaling; single point of failure  
**Description**: MADAR is configured for single-instance deployment. There is no Kubernetes, Docker Swarm, or multi-instance setup provided. The PostgreSQL and Redis instances are shared across the single API instance.  
**Workaround**: None for v1.0.0-rc1. Deploy on a VM or container host with adequate resources.  
**Planned for**: v2.0.0

### INF-02 — Docker Networking Requires Manual Reconnect After Port Collision
**Severity**: Low  
**Impact**: API container may start without network attachment if port 8000 is already bound  
**Description**: If port 8000 is in use when `docker compose up` runs, the API container starts but fails to attach to the Docker bridge network. Requires `docker network connect madar_default madar-api-1`.  
**Workaround**: Kill any process on port 8000 before running `docker compose up`: `lsof -ti:8000 | xargs kill -9 2>/dev/null`  
**Planned for**: v1.1.0 — Add pre-start healthcheck or port validation script

### INF-03 — No TLS/HTTPS Included
**Severity**: Medium  
**Impact**: Traffic is unencrypted in the default setup  
**Description**: No reverse proxy (Nginx/Traefik) configuration is included. TLS must be configured externally.  
**Workaround**: Place Nginx or Traefik in front of the Docker stack and configure HTTPS.  
**Planned for**: v1.1.0 — Add example Nginx + Certbot configuration

### INF-04 — No Log Aggregation
**Severity**: Low  
**Impact**: Logs are written to Docker stdout only  
**Description**: No centralized logging configuration (ELK, Loki, CloudWatch, etc.) is provided.  
**Workaround**: Use `docker compose logs -f` or attach a log driver in `docker-compose.yml`.  
**Planned for**: v1.2.0

---

## API / Backend Limitations

### API-01 — `datetime.utcnow()` Deprecation Warnings
**Severity**: Low  
**Impact**: 249 DeprecationWarnings in test output; no functional impact  
**Description**: Python 3.12 deprecates `datetime.datetime.utcnow()`. Several service files use this function for `deleted_at` timestamps.  
**Affected files**: `master_data_service.py`, `crm_service.py`  
**Workaround**: No action required; functionality is correct  
**Planned for**: v1.1.0 — Replace with `datetime.now(datetime.UTC)`

### API-02 — No API Rate Limiting
**Severity**: Medium  
**Impact**: API is vulnerable to high-frequency requests / basic DoS  
**Description**: No request rate limiting is implemented at the API level. All endpoints accept unlimited requests.  
**Workaround**: Implement rate limiting at the reverse proxy/WAF layer.  
**Planned for**: v1.1.0 — Add `slowapi` or similar middleware

### API-03 — No Pagination on List Endpoints
**Severity**: Medium  
**Impact**: Large datasets will cause slow responses and high memory usage  
**Description**: List endpoints (branches, customers, products, etc.) return all records without pagination. With 10,000+ records, response times will degrade.  
**Workaround**: Limit data volume in production until pagination is implemented.  
**Planned for**: v1.1.0 — Add `limit`/`offset` parameters to all list endpoints

### API-04 — Soft-Delete Filters Not Applied Consistently
**Severity**: Low  
**Impact**: Deleted items may appear in some list queries  
**Description**: Not all service methods consistently filter `is_deleted=False`. Some raw queries may return soft-deleted records.  
**Workaround**: Manually verify list endpoints return only active records.  
**Planned for**: v1.1.0 — Add global SQLAlchemy query filter for `is_deleted`

### API-05 — No File Upload Support
**Severity**: Low  
**Impact**: Product images and documents cannot be attached  
**Description**: The `Product` model has an `image_url` field but no file upload endpoint exists.  
**Workaround**: Provide externally-hosted image URLs manually.  
**Planned for**: v1.2.0

### API-06 — No Email Notifications
**Severity**: Low  
**Impact**: No automated emails for registration, invoices, or alerts  
**Description**: The system does not send any email notifications. No SMTP configuration is included.  
**Workaround**: Manual notification outside the system.  
**Planned for**: v1.2.0

---

## Frontend Limitations

### FE-01 — No Pagination in UI Tables
**Severity**: Medium  
**Impact**: Tables show all records; becomes unusable with large datasets  
**Description**: All list pages (branches, customers, products, etc.) load all records into the table without pagination, infinite scroll, or virtual scrolling.  
**Workaround**: Keep dataset small during RC testing.  
**Planned for**: v1.1.0 — Add server-side pagination to all tables

### FE-02 — No Real-Time Updates (WebSocket / SSE)
**Severity**: Low  
**Impact**: Dashboard KPIs require manual page refresh to update  
**Description**: Frontend uses REST polling only; no WebSocket or Server-Sent Events for real-time data.  
**Workaround**: Manually refresh the page to see updated data.  
**Planned for**: v1.2.0

### FE-03 — No Bulk Operations
**Severity**: Low  
**Impact**: Cannot delete/update multiple records simultaneously  
**Description**: All CRUD pages support single-record operations only. No checkboxes, select-all, or bulk delete.  
**Planned for**: v1.2.0

### FE-04 — Limited Form Validation Feedback
**Severity**: Low  
**Impact**: Some validation error messages from API are not displayed in the UI  
**Description**: API returns structured 422 error responses but the frontend may display generic error messages.  
**Workaround**: Check the browser's developer console for detailed API error responses.  
**Planned for**: v1.1.0

### FE-05 — No Offline / PWA Support
**Severity**: Low  
**Impact**: Application is not functional without network connectivity  
**Description**: No service worker or offline caching is implemented.  
**Planned for**: v2.0.0

---

## Security Limitations

### SEC-01 — Default JWT Secret in .env.example
**Severity**: **High** (if not changed before production use)  
**Impact**: Tokens can be forged if the default secret is used in production  
**Description**: `JWT_SECRET_KEY=change-this-secret-key-in-production` is the default value in `.env.example`. If copied verbatim to production, any party knowing this value can forge valid JWT tokens.  
**Workaround**: **MUST change** before any production deployment. Generate with: `openssl rand -hex 32`  
**Status**: Documented in INSTALL.md and SECURITY_CHECKLIST.md

### SEC-02 — No CSRF Protection for Browser Clients
**Severity**: Low (mitigated by JWT auth)  
**Impact**: Potential CSRF attacks on stateful cookie-based auth (not currently used)  
**Description**: No CSRF token middleware is configured. However, the application uses JWT Bearer tokens (not cookies) by default, which mitigates CSRF.  
**Planned for**: v1.1.0 — Add CSRF middleware if cookie auth is ever implemented

### SEC-03 — npm Dependency Vulnerabilities
**Severity**: Medium  
**Impact**: 5 npm vulnerabilities (1 moderate, 3 high, 1 critical) in frontend dependencies  
**Description**: Running `npm audit` reports vulnerabilities in transitive frontend dependencies. These are in dev/build dependencies (Next.js ecosystem) and not directly exploitable at runtime.  
**Workaround**: Run `npm audit fix` to resolve auto-fixable issues; review the critical one manually.  
**Planned for**: v1.1.0 — Update dependency versions

---

## Data / Database Limitations

### DB-01 — No Database Backup Strategy Included
**Severity**: Medium  
**Impact**: Risk of data loss without external backup configuration  
**Description**: No `pg_dump` scripts, backup schedules, or point-in-time recovery configuration is provided.  
**Workaround**: Implement `pg_dump` cron job manually or use a managed PostgreSQL service with built-in backups.  
**Planned for**: v1.1.0 — Add backup script and documentation

### DB-02 — Soft Delete Not Reversible via API
**Severity**: Low  
**Impact**: Deleted records cannot be restored through the UI or API  
**Description**: Records are soft-deleted (`is_deleted=true`) but there is no API endpoint or UI to restore them.  
**Workaround**: Restore via direct database query: `UPDATE table SET is_deleted=false WHERE id=X`  
**Planned for**: v1.2.0 — Add restore endpoints

### DB-03 — No Audit Log UI
**Severity**: Low  
**Impact**: `audit_logs` table exists but is not exposed in the API or frontend  
**Description**: The `audit_logs` table is created by migration 20260718_000014 but no service, route, or UI page reads from it.  
**Planned for**: v1.2.0 — Implement audit trail API and UI

---

## Documentation Limitations

### DOC-01 — Screenshots Not Yet Generated
**Severity**: Low  
**Impact**: README and release notes lack visual documentation  
**Description**: `SCREENSHOTS_GUIDE.md` documents how to create screenshots, but actual screenshots have not been generated and added to `docs/screenshots/`.  
**Workaround**: Follow `docs/SCREENSHOTS_GUIDE.md` to generate screenshots manually.  
**Planned for**: Before stable v1.0.0 release

### DOC-02 — API Documentation Has No Authentication Examples in Some Endpoints
**Severity**: Low  
**Impact**: Some Swagger/OpenAPI endpoint examples do not show complete request/response samples  
**Description**: Auto-generated Swagger UI is complete but some endpoints lack rich example values.  
**Planned for**: v1.1.0 — Add `openapi_examples` to key endpoints

---

## Feature Gaps (Intentionally Out of Scope for RC1)

The following features are in the backlog but deliberately excluded from this release per the **"do not implement new business modules"** directive:

| Feature | Status | Target |
|---------|--------|--------|
| Advanced reporting / exports | Deferred | v1.2.0 |
| Purchase order management | Schema only | v1.2.0 |
| Mobile application | Not started | v2.0.0 |
| Payment gateway integration | Not started | v2.0.0 |
| Multi-language UI (beyond Arabic) | Partial | v1.1.0 |
| Advanced inventory forecasting | Not started | v2.0.0 |
| HR payroll calculations | Schema only | v1.2.0 |
| Fixed assets depreciation | Schema only | v1.2.0 |
| Chart of Accounts transactions | Schema only | v1.1.0 |
| CRM email integration | Not started | v1.2.0 |

---

## Resolved Issues (Fixed in RC1)

The following issues were identified during validation and resolved before RC1 tagging:

| ID | Issue | Status |
|----|-------|--------|
| FIX-01 | Frontend Docker build fails (missing package-lock.json) | ✅ Fixed |
| FIX-02 | Frontend Docker build fails (missing public/ directory) | ✅ Fixed |
| FIX-03 | API Docker env_file loaded .env.example instead of .env | ✅ Fixed |
| FIX-04 | Seed script not copied into Docker image | ✅ Fixed |
| FIX-05 | Seed script Company model field mismatches | ✅ Fixed |
| FIX-06 | Seed script Warehouse model field mismatches | ✅ Fixed |
| FIX-07 | Seed script SalesQuotation/Order/Invoice field mismatches | ✅ Fixed |
| FIX-08 | POST /branches returns 500 on invalid input (no Pydantic schema) | ✅ Fixed |

---

## Reporting New Issues

Please report new issues at: https://github.com/mdardash-star/MADAR/issues

Use the appropriate template:
- **Bug Report**: For unexpected behavior
- **Feature Request**: For new capabilities
- **General**: For questions or discussions
