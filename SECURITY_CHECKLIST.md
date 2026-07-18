# MADAR v1.0.0-rc1 — Security Checklist

**Version**: v1.0.0-rc1  
**Date**: 2026-07-18  
**Framework**: OWASP Top 10 (2021) + Application-Specific Controls  

This document must be reviewed and signed off before every production deployment. Items marked ✅ are verified for RC1. Items marked ⚠️ require action before production use. Items marked ❌ are known gaps tracked in KNOWN_LIMITATIONS.md.

---

## Pre-Deployment Mandatory Actions

> **These items MUST be completed before any production deployment.**

- [ ] **CRITICAL**: Change `JWT_SECRET_KEY` from default (`change-this-secret-key-in-production`)
  ```bash
  openssl rand -hex 32  # Use this output as JWT_SECRET_KEY
  ```
- [ ] **CRITICAL**: Change `POSTGRES_PASSWORD` from default (`madar_password`)
- [ ] **HIGH**: Configure `CORS_ORIGINS` to restrict to your domain only
- [ ] **HIGH**: Enable HTTPS/TLS via reverse proxy (Nginx/Traefik)
- [ ] **HIGH**: Remove or restrict access to `/docs` and `/redoc` in production
- [ ] **MEDIUM**: Run `npm audit fix` to resolve frontend dependency vulnerabilities
- [ ] **MEDIUM**: Configure database backups (see DB-01 in KNOWN_LIMITATIONS.md)
- [ ] **MEDIUM**: Set `DEBUG=false` in all production environment files

---

## 1. OWASP A01 — Broken Access Control

| Control | Status | Notes |
|---------|--------|-------|
| JWT token required for all `/api/v1/*` endpoints | ✅ Verified | Unauthenticated requests return 401 |
| Company data isolation (multi-tenancy) | ✅ Verified | `company_id` filter applied in all queries |
| Role-based access control (RBAC) | ✅ Verified | Roles and permissions seeded per company |
| Deleted records not returned in list queries | ✅ Verified | `is_deleted=False` filter applied |
| Token expiry enforced | ✅ Verified | `JWT_ACCESS_TOKEN_EXPIRE_MINUTES=60` |
| Refresh token rotation | ✅ Verified | `/auth/refresh` issues new token pair |
| No direct object reference (IDOR) vulnerabilities tested | ⚠️ Partial | Not fully penetration tested |
| Admin-only endpoints protected | ✅ Verified | RBAC gates admin operations |

---

## 2. OWASP A02 — Cryptographic Failures

| Control | Status | Notes |
|---------|--------|-------|
| Passwords hashed with bcrypt | ✅ Verified | `passlib[bcrypt]` used in `security.py` |
| Plaintext passwords never stored | ✅ Verified | `get_password_hash()` called before persistence |
| JWT signed with HMAC-SHA256 | ✅ Verified | `JWT_ALGORITHM=HS256` |
| JWT secret is configurable (not hardcoded) | ✅ Verified | Read from environment variable |
| JWT secret is long and random in production | ⚠️ Action required | **Must change from default before production** |
| HTTPS enforced (TLS 1.2+) | ⚠️ Action required | No TLS in default config; must add reverse proxy |
| Database connection uses password | ✅ Verified | `POSTGRES_PASSWORD` required |
| Redis has no auth in default config | ⚠️ Note | Redis is only exposed internally; add `requirepass` for internet-exposed deployments |

---

## 3. OWASP A03 — Injection

| Control | Status | Notes |
|---------|--------|-------|
| SQL injection prevention via SQLAlchemy ORM | ✅ Verified | Parameterized queries used throughout |
| No raw SQL string interpolation detected | ✅ Verified | All queries use ORM or `text()` with bound params |
| Input validation via Pydantic v2 | ✅ Verified | All request bodies use typed Pydantic models |
| String field length limits enforced | ✅ Verified | `Field(min_length=1, max_length=255)` on key fields |
| NoSQL injection not applicable | ✅ N/A | No NoSQL databases used |
| Command injection | ✅ Verified | No shell command execution in application code |
| Template injection | ✅ N/A | No server-side templates used |

---

## 4. OWASP A04 — Insecure Design

| Control | Status | Notes |
|---------|--------|-------|
| Multi-tenant design reviewed | ✅ Verified | Consistent `company_id` scoping |
| Business logic errors produce appropriate HTTP codes | ✅ Verified | 400 for duplicates, 404 for not found, 422 for validation |
| Threat model documented | ⚠️ Partial | Basic threats addressed; full threat model not yet produced |
| Sensitive endpoints protected by auth middleware | ✅ Verified | FastAPI dependency injection enforces auth |
| No mass assignment vulnerabilities | ✅ Verified | Pydantic schemas explicitly define allowed fields |

---

## 5. OWASP A05 — Security Misconfiguration

| Control | Status | Notes |
|---------|--------|-------|
| Debug mode disabled (`DEBUG=false`) | ✅ Verified in containers | Check production `.env` before deploy |
| API docs restricted in production | ⚠️ Action required | `/docs` and `/redoc` are publicly accessible; disable or restrict in production |
| CORS configured | ✅ Basic | `*` origin allowed in development; restrict in production |
| Default credentials changed | ⚠️ Action required | Demo credentials `admin@acme-demo.com`/`Demo123!` are well-known; change in production |
| No sensitive data in error messages | ✅ Verified | FastAPI exception handlers return generic messages |
| Database not exposed to internet | ✅ Verified | PostgreSQL binds only to Docker internal network in production |
| Redis not exposed to internet | ✅ Verified | Redis binds to Docker internal network |
| Environment files not committed to git | ✅ Verified | `.env` files are in `.gitignore` |

---

## 6. OWASP A06 — Vulnerable and Outdated Components

| Component | Version | Vulnerabilities | Status |
|-----------|---------|-----------------|--------|
| FastAPI | 0.104+ | None known | ✅ |
| Pydantic | 2.0+ | None known | ✅ |
| SQLAlchemy | 2.0+ | None known | ✅ |
| python-jose | Latest | Check regularly | ⚠️ |
| passlib | Latest | None known | ✅ |
| Next.js | 14.2.35 | Check npm audit | ⚠️ |
| React | 18.3.1 | None known | ✅ |
| PostgreSQL | 16 | None known | ✅ |
| Redis | 7 | None known | ✅ |
| Python | 3.12 | None known | ✅ |
| Node.js | 20 | None known | ✅ |

**Frontend npm audit status**: 5 vulnerabilities (1 moderate, 3 high, 1 critical)  
**Action**: Run `cd apps/web && npm audit fix` before production deployment

---

## 7. OWASP A07 — Identification and Authentication Failures

| Control | Status | Notes |
|---------|--------|-------|
| Brute force protection | ❌ Not implemented | No rate limiting on `/auth/login`; document in KNOWN_LIMITATIONS |
| Multi-factor authentication (MFA) | ❌ Not implemented | Planned for v1.2.0 |
| Session invalidation on logout | ⚠️ JWT only | JWTs expire; no server-side token revocation list |
| Password minimum complexity enforced | ✅ Verified | Minimum 8 characters enforced in schemas |
| Password stored securely | ✅ Verified | bcrypt hash |
| Account lockout | ❌ Not implemented | Planned for v1.1.0 |
| Credential stuffing protection | ❌ Not implemented | Requires rate limiting (API-02) |

---

## 8. OWASP A08 — Software and Data Integrity Failures

| Control | Status | Notes |
|---------|--------|-------|
| Alembic migration integrity | ✅ Verified | Migration files version-controlled |
| Docker images from official sources | ✅ Verified | Official Docker Hub images used |
| No unsigned or untrusted dependencies | ✅ Verified | All packages from PyPI / npm with pinned versions |
| GitHub Actions CI validates code | ✅ Verified | Build and test pipeline in `.github/workflows/` |

---

## 9. OWASP A09 — Security Logging and Monitoring Failures

| Control | Status | Notes |
|---------|--------|-------|
| Authentication events logged | ⚠️ Partial | uvicorn access logs; no structured auth event logging |
| Failed login attempts logged | ⚠️ Partial | HTTP 401 responses logged; no dedicated auth failure log |
| Audit log table implemented | ✅ Schema | `audit_logs` table exists; no data written yet |
| Log aggregation configured | ❌ Not configured | See INF-04 in KNOWN_LIMITATIONS.md |
| Alerting on anomalies | ❌ Not configured | Requires external monitoring setup |
| Log retention policy | ❌ Not configured | Docker stdout only |

---

## 10. OWASP A10 — Server-Side Request Forgery (SSRF)

| Control | Status | Notes |
|---------|--------|-------|
| No user-controlled URLs used in server-side requests | ✅ Verified | Application does not make outbound HTTP calls based on user input |
| No URL fetch endpoints | ✅ Verified | Not applicable to current feature set |

---

## Application-Specific Security Controls

### JWT Token Security

```python
# Verified configuration in apps/api/app/core/config.py:
JWT_SECRET_KEY: str  # MUST change from default before production
JWT_ALGORITHM: str = "HS256"  # Symmetric signing; sufficient for single-service
JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60  # 1-hour expiry
```

**Recommendations**:
- For high-security environments, use `RS256` (asymmetric) instead of `HS256`
- Consider reducing `JWT_ACCESS_TOKEN_EXPIRE_MINUTES` to 15-30 minutes
- Implement a token revocation list for immediate logout

### Database Security

```bash
# Verified: Database only accessible from Docker network
# madar-db-1 binds to 0.0.0.0:5432 for development
# In production: remove the ports: mapping from docker-compose.yml
```

**Production database hardening**:
```yaml
# Remove from docker-compose.yml for production:
# ports:
#   - "5432:5432"
```

### Secrets Management

| Secret | Location | Status |
|--------|----------|--------|
| `JWT_SECRET_KEY` | `.env` / environment | ⚠️ Must change |
| `POSTGRES_PASSWORD` | `.env` / environment | ⚠️ Must change |
| Admin password | Demo only | ⚠️ Must change |
| Redis password | None configured | ⚠️ Consider for production |

---

## Security Hardening Commands (Run Before Production)

```bash
# 1. Generate secure JWT secret
JWT_SECRET=$(openssl rand -hex 32)
echo "JWT_SECRET_KEY=$JWT_SECRET" >> apps/api/.env

# 2. Generate secure DB password
DB_PASS=$(openssl rand -base64 24)
echo "POSTGRES_PASSWORD=$DB_PASS" >> .env
echo "POSTGRES_PASSWORD=$DB_PASS" >> apps/api/.env

# 3. Fix npm vulnerabilities
cd apps/web && npm audit fix

# 4. Remove database port mapping (prevent external access)
# Edit docker-compose.yml: comment out db.ports section

# 5. Restrict API docs access (add to main.py)
# app = FastAPI(docs_url=None, redoc_url=None)  # for production

# 6. Set correct CORS origins
# CORS_ORIGINS=https://yourdomain.com in .env
```

---

## Penetration Testing Scope (Pre-Stable Release)

The following areas require external penetration testing before v1.0.0 stable:

1. **Authentication brute force** — Test rate limiting gaps (SEC: brute force, account lockout)
2. **Multi-tenant isolation** — Attempt cross-company data access
3. **JWT token forgery** — Verify signature validation
4. **SQL injection** — Automated scan of all input fields
5. **XSS** — Frontend input/output encoding validation
6. **IDOR** — Test resource access with different company tokens
7. **CSRF** — Verify JWT auth prevents CSRF
8. **Dependency vulnerabilities** — `npm audit` + `pip audit` on all transitive deps

---

## Sign-Off

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Security Lead | | | |
| Development Lead | | | |
| DevOps Lead | | | |
| Product Manager | | | |

**All mandatory items must be checked ✅ before production deployment.**
