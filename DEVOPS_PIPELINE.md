# MADAR — DevOps Pipeline

**Version**: 1.0  
**Date**: 2026-07-18  
**Status**: Active  
**Owner**: DevOps Lead  

---

## 1. Pipeline Overview

```
Developer
   │
   ├── git push feature/* 
   │       └── [CI: lint + test + build]
   │
   ├── PR → develop
   │       └── [CI: full suite + preview deploy]
   │
   ├── merge to develop
   │       └── [CI + CD: auto-deploy to staging]
   │
   └── merge to main (after staging approval)
           └── [CI + CD: manual-approve → production deploy]
```

---

## 2. GitHub Actions Workflows

### 2.1 CI Pipeline (`.github/workflows/ci.yml`)

Triggers on every push and PR. Runs in parallel:

**Backend job:**
1. Checkout code
2. Python 3.12 setup
3. `pip install -r requirements.txt`
4. `ruff check .` — lint
5. `pytest -q` — unit + integration tests
6. Upload test coverage artifact

**Frontend job:**
1. Checkout code  
2. Node.js 20 setup with npm cache
3. `npm ci`
4. `npm run build` — TypeScript compile + Next.js build
5. Upload build artifact

### 2.2 CD Pipeline (`.github/workflows/deploy.yml`)

**Staging** (auto-deploy on merge to `develop`):
1. CI must pass
2. Build Docker images + push to GHCR
3. SSH to staging server
4. `docker compose pull && docker compose up -d`
5. Run migrations
6. Smoke test (curl /health)
7. Notify Slack

**Production** (manual approval gate on merge to `main`):
1. CI must pass
2. Build + push Docker images tagged with git SHA and semver
3. **Manual approval step** (GitHub Environment protection rule)
4. SSH to production server
5. `docker compose pull && docker compose up -d --no-deps api`
6. Health check loop (5 retries, 10s apart)
7. Run migrations
8. `docker compose up -d --no-deps web`
9. Full smoke test
10. Notify Slack + PagerDuty

### 2.3 Maintenance Workflows

**Backup** (`.github/workflows/backup.yml`):
- Schedule: `0 2 * * *` (2:00 AM UTC daily)
- `pg_dump` → compress → upload to S3
- Verify backup integrity
- Notify on failure

**SSL Renewal** (`.github/workflows/ssl-renew.yml`):
- Schedule: `0 3 1 * *` (1st of month, 3:00 AM)
- `certbot renew --nginx`
- Restart Nginx
- Verify certificate

**Dependency Updates** (`.github/workflows/deps.yml`):
- Schedule: Weekly (Monday 9:00 AM)
- `pip-audit` for Python CVEs
- `npm audit` for JS CVEs
- Create PR if vulnerabilities found

---

## 3. Docker Registry

```bash
# GitHub Container Registry (GHCR) — free for public repos
ghcr.io/mdardash-star/madar-api:latest
ghcr.io/mdardash-star/madar-api:v1.0.0-rc1
ghcr.io/mdardash-star/madar-api:sha-cc5adcd

ghcr.io/mdardash-star/madar-web:latest
ghcr.io/mdardash-star/madar-web:v1.0.0-rc1
```

### Image Tagging Strategy

```
:latest          → most recent main branch build
:v{semver}       → versioned release (e.g., v1.0.0)
:sha-{8chars}    → exact commit SHA for rollbacks
:develop         → latest develop branch
```

---

## 4. Secrets Management

### GitHub Secrets (CI/CD)

Configure in: GitHub → Settings → Secrets and variables → Actions

| Secret Name | Value | Used By |
|-------------|-------|---------|
| `PROD_SSH_KEY` | Private key for prod server | deploy.yml |
| `PROD_HOST` | Production server IP/hostname | deploy.yml |
| `PROD_USER` | SSH username (ubuntu) | deploy.yml |
| `STAGING_SSH_KEY` | Private key for staging server | deploy.yml |
| `STAGING_HOST` | Staging server IP/hostname | deploy.yml |
| `SLACK_WEBHOOK` | Slack notification webhook | All workflows |
| `GHCR_TOKEN` | GitHub Container Registry token | deploy.yml |
| `S3_BACKUP_KEY` | AWS/DO S3 access key | backup.yml |
| `S3_BACKUP_SECRET` | AWS/DO S3 secret | backup.yml |
| `SENTRY_DSN` | Error tracking DSN | deploy.yml |

### Production Server Secrets

```bash
# On production server — never committed to git
/opt/madar/.env.production

# Managed by: HashiCorp Vault (Phase 2) or AWS Secrets Manager
# Current: Encrypted file in /opt/madar/secrets/ (chmod 600)
```

---

## 5. Environment Promotion Flow

```
Feature branch
     │ PR review + CI pass
     ▼
develop branch
     │ Auto-deploy → staging
     │ QA sign-off
     ▼
main branch
     │ Manual approval (Product Manager + DevOps Lead)
     │ Deploy → production
     │ 15-min monitoring watch
     ▼
v{semver} tag
     │ GitHub Release created
     │ CHANGELOG updated
```

---

## 6. Deployment Environments

### Staging Server

```yaml
# .env.staging
APP_ENV=staging
DEBUG=false
LOG_LEVEL=INFO
POSTGRES_DB=madar_staging
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=60
CORS_ORIGINS=https://staging.madar.app
SENTRY_ENVIRONMENT=staging
```

### Production Server

```yaml
# .env.production  
APP_ENV=production
DEBUG=false
LOG_LEVEL=WARNING
POSTGRES_DB=madar_prod
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30  # shorter for production
CORS_ORIGINS=https://app.madar.app
SENTRY_ENVIRONMENT=production
API_WORKERS=2  # uvicorn --workers 2
```

---

## 7. Rollback Strategy

### Automatic Rollback Triggers
- Health check fails after deploy (5 retries × 10s)
- Error rate > 5% in 5-minute window post-deploy
- Response time p95 > 2 seconds post-deploy

### Manual Rollback Commands

```bash
# Option 1: Re-deploy previous image tag
cd /opt/madar
DEPLOY_TAG=sha-abc1234 docker compose -f docker-compose.prod.yml up -d

# Option 2: Git rollback
git checkout v1.0.0-rc1
docker compose -f docker-compose.prod.yml up -d --build

# Option 3: Database rollback (if migration was applied)
docker compose -f docker-compose.prod.yml exec api alembic downgrade -1
```

---

## 8. Quality Gates

### Pre-merge to `develop`
- [ ] All CI checks green
- [ ] PR reviewed by at least 1 engineer
- [ ] No new security vulnerabilities (pip-audit, npm audit)

### Pre-merge to `main`  
- [ ] All CI checks green
- [ ] Staging deployed and smoke-tested
- [ ] QA sign-off (manual testing checklist)
- [ ] No open P1/P2 bugs

### Pre-release tag
- [ ] RELEASE_VALIDATION.md completed
- [ ] KNOWN_LIMITATIONS.md updated
- [ ] CHANGELOG.md updated
- [ ] Performance baseline not regressed

---

## 9. Monitoring the Pipeline

| Signal | Source | Alert Threshold |
|--------|--------|-----------------|
| CI failure rate | GitHub Actions | > 20% over 7 days |
| Deploy frequency | GitHub Actions | < 1/week (low velocity) |
| Build time | GitHub Actions | > 10 min (optimization needed) |
| Test coverage | pytest-cov | < 70% (block merge) |
| Deployment lead time | CI start → prod deploy | > 2 hours (process review) |

---

## 10. Operational Runbook Locations

| Topic | Location |
|-------|----------|
| Deployment procedure | `DEPLOYMENT_PLAN.md` |
| Incident response | `INCIDENT_RESPONSE.md` |
| Backup + restore | `BACKUP_AND_RECOVERY.md` |
| Monitoring alerts | `MONITORING.md` |
| On-call escalation | `INCIDENT_RESPONSE.md` |
