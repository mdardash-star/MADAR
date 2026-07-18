# MADAR — Incident Response

**Version**: 1.0  
**Date**: 2026-07-18  
**Status**: Active  
**Owner**: DevOps Lead + CTO  

---

## 1. Incident Classification

| Severity | Definition | Examples | Response SLA |
|----------|------------|---------|-------------|
| **P1 — Critical** | Full service outage or data loss | API down, DB down, data breach | Immediate (24/7) |
| **P2 — High** | Partial outage or major degradation | Auth broken, error rate > 5% | 1 hour |
| **P3 — Medium** | Single feature broken, performance degraded | Reports slow, specific endpoint failing | 4 hours |
| **P4 — Low** | Minor issue, minimal user impact | UI bug, slow non-critical endpoint | Next business day |

---

## 2. Incident Response Team

| Role | Responsibility | Escalation Path |
|------|----------------|-----------------|
| **On-Call Engineer** | First responder, initial triage | Primary contact |
| **Incident Commander (IC)** | Coordinate response, communication | DevOps Lead or CTO |
| **Technical Lead** | Deep technical investigation | Assigned by IC |
| **Communications Lead** | Customer/stakeholder updates | Product Manager |
| **Executive** | Business decisions, external escalation | CTO |

---

## 3. Incident Response Process

```
ALERT TRIGGERED (Prometheus / UptimeRobot / Customer report)
         │
         ▼
ACKNOWLEDGE within response SLA
         │
         ▼
TRIAGE: Assess severity (P1-P4)
  ├── P1/P2: Page on-call immediately
  └── P3/P4: Log in issue tracker, schedule
         │
         ▼
NOTIFY: Slack #incident channel
  Template: "🚨 P{N} INCIDENT: {brief description}
             Started: {time}
             Impact: {who is affected}
             IC: {name}
             Status: INVESTIGATING"
         │
         ▼
INVESTIGATE
  1. Check Grafana dashboards
  2. Check Loki logs (search "level=error")
  3. Check Sentry for new exceptions
  4. Check docker compose ps
  5. Check recent deployments
         │
         ▼
MITIGATE (restore service ASAP, even if root cause unknown)
  Options:
  ├── Rollback to previous deployment
  ├── Restart failing container
  ├── Scale resources
  └── Disable affected feature (feature flag)
         │
         ▼
RESOLVE
  - Update Slack: "✅ RESOLVED: {what was done}"
  - Update status page
  - Notify affected customers
         │
         ▼
POSTMORTEM (within 48 hours for P1/P2)
  - Timeline
  - Root cause analysis
  - Impact analysis
  - Action items with owners and due dates
```

---

## 4. Common Incident Runbooks

### 4.1 API Service Down

```bash
# Step 1: Verify the issue
curl -f http://localhost:8000/health
# Expected: {"status":"healthy"}
# If no response: service is down

# Step 2: Check container status
docker compose -f /opt/madar/docker-compose.prod.yml ps

# Step 3: Check recent logs
docker compose -f /opt/madar/docker-compose.prod.yml logs api --tail=100

# Step 4: Restart if crash-looping
docker compose -f /opt/madar/docker-compose.prod.yml restart api

# Step 5: If restart doesn't help, rollback last deployment
cd /opt/madar
git log --oneline -5
git checkout {previous-working-commit}
docker compose -f docker-compose.prod.yml up -d --build api
```

### 4.2 Database Connection Failures

```bash
# Step 1: Verify PostgreSQL is up
docker compose -f /opt/madar/docker-compose.prod.yml ps db
docker compose -f /opt/madar/docker-compose.prod.yml logs db --tail=50

# Step 2: Test connection directly
docker compose -f /opt/madar/docker-compose.prod.yml exec db \
  pg_isready -U madar -d madar_prod

# Step 3: Check for long-running queries blocking connections
docker compose -f /opt/madar/docker-compose.prod.yml exec db psql -U madar -c \
  "SELECT pid, now()-query_start AS duration, state, query FROM pg_stat_activity 
   WHERE state != 'idle' ORDER BY duration DESC LIMIT 10;"

# Step 4: Kill blocking queries if necessary
docker compose -f /opt/madar/docker-compose.prod.yml exec db psql -U madar -c \
  "SELECT pg_terminate_backend(pid) FROM pg_stat_activity 
   WHERE (now()-query_start) > interval '10 minutes' AND state='active';"

# Step 5: Restart PostgreSQL (last resort)
docker compose -f /opt/madar/docker-compose.prod.yml restart db
# Wait for healthcheck
sleep 30
docker compose -f /opt/madar/docker-compose.prod.yml restart api
```

### 4.3 High Error Rate (5xx)

```bash
# Step 1: Identify which endpoints are failing
# In Grafana: HTTP Error Rate dashboard
# In Loki: {job="madar-api"} |= "level=error"

# Step 2: Check for recent code deployment
git log --oneline -5
# If deployed recently: rollback

# Step 3: Check for database errors
docker compose logs api 2>&1 | grep -i "sqlalchemy\|postgres\|connection"

# Step 4: Check for memory pressure
docker stats --no-stream

# Step 5: Temporary mitigation — increase workers
# Edit docker-compose.prod.yml: command: uvicorn app.main:app --workers 4
docker compose -f docker-compose.prod.yml up -d --no-deps api
```

### 4.4 High Latency (p95 > 2s)

```bash
# Step 1: Identify slow endpoints
# In Grafana: Request Duration dashboard

# Step 2: Check database slow queries
docker compose exec db psql -U madar -c \
  "SELECT query, mean_exec_time, calls 
   FROM pg_stat_statements 
   ORDER BY mean_exec_time DESC LIMIT 10;"

# Step 3: Check for missing indexes (EXPLAIN ANALYZE)
docker compose exec db psql -U madar -c \
  "EXPLAIN (ANALYZE, BUFFERS) SELECT * FROM products WHERE company_id=1;"

# Step 4: Check Redis cache hit rate
docker compose exec redis redis-cli info stats | grep -E "keyspace_hits|keyspace_misses"

# Step 5: Scale API workers if CPU-bound
# Edit docker-compose.prod.yml: command: uvicorn --workers 4
```

### 4.5 Disk Space Low (< 20%)

```bash
# Step 1: Find what's consuming space
df -h
du -sh /var/lib/docker/*
du -sh /opt/madar/backups/*

# Step 2: Clean Docker images/containers
docker system prune -f
docker image prune -a -f

# Step 3: Clean old backups
find /opt/madar/backups -name "*.sql.gz" -mtime +7 -delete

# Step 4: Clean PostgreSQL WAL files (if archive_mode is on)
docker compose exec db psql -U madar -c "CHECKPOINT;"
docker compose exec db psql -U madar -c "SELECT pg_switch_wal();"

# Step 5: Scale disk volume (cloud provider) or add EBS volume
```

### 4.6 Memory Exhaustion

```bash
# Step 1: Identify memory consumers
docker stats --no-stream | sort -k 7 -rn

# Step 2: Check for Python memory leak in API
docker compose exec api python -c \
  "import tracemalloc; tracemalloc.start(); print('tracing started')"

# Step 3: Restart API to clear memory leak
docker compose -f docker-compose.prod.yml restart api

# Step 4: Adjust PostgreSQL shared_buffers if DB is the culprit
# Reduce: shared_buffers = 512MB (from 2GB)
# Restart: docker compose restart db

# Step 5: Add swap space as emergency measure
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

### 4.7 Security Incident (Suspected Breach)

```bash
# IMMEDIATELY:
# 1. Page CTO + DevOps Lead (P1 escalation)
# 2. DO NOT take the system offline yet — preserve logs

# Step 1: Preserve all logs
docker compose logs > /tmp/incident-$(date +%Y%m%d-%H%M%S).log
cp /var/log/nginx/access.log /tmp/nginx-$(date +%Y%m%d).log

# Step 2: Block attacker IP (if identified)
# In Cloudflare: Security → IP Access Rules → Block
# In Nginx: Add to deny list

# Step 3: Rotate compromised secrets
openssl rand -hex 32 > /tmp/new-jwt-secret.txt
# Update JWT_SECRET_KEY in .env.production
# Restart API: docker compose restart api
# All existing tokens immediately invalidated

# Step 4: Force all users to re-login
# Update JWT_SECRET_KEY to new value (all sessions invalidated)

# Step 5: Audit what was accessed
docker compose exec db psql -U madar -c \
  "SELECT * FROM audit_logs WHERE created_at > now() - interval '24 hours' ORDER BY created_at DESC;"

# Step 6: Notify legal/compliance team
# Prepare incident report for GDPR/PDPL notification requirements
```

---

## 5. Communication Templates

### Internal Slack Notification

```
🚨 P{SEVERITY} INCIDENT OPENED

Summary: {brief description}
Started: {ISO timestamp}
Impact: {who/what is affected}
Incident Commander: @{name}
Status: INVESTIGATING

Dashboard: https://grafana.internal/d/madar-overview
Logs: https://grafana.internal/d/loki-search
```

### Customer Status Page Update

```
[Investigating] We are investigating reports of {feature/service}
experiencing issues. Our team has been notified and is actively
working on a resolution. We will provide an update within 30 minutes.

Started: {time}
Affected: {service name}
Status: Investigating
```

### Resolution Notification

```
[Resolved] The {feature/service} issue has been resolved.
Root cause: {brief description}
Duration: {X minutes/hours}
We apologize for the disruption to your service.
```

---

## 6. Postmortem Template

```markdown
# Incident Postmortem — {Title}

**Date**: {date}
**Severity**: P{N}
**Duration**: {start} → {end} ({duration})
**Impact**: {number of affected customers/companies/requests}
**Incident Commander**: {name}

## Timeline

| Time | Event |
|------|-------|
| HH:MM | Alert triggered |
| HH:MM | On-call acknowledged |
| HH:MM | Root cause identified |
| HH:MM | Mitigation applied |
| HH:MM | Incident resolved |

## Root Cause

{Detailed technical explanation of what went wrong and why}

## Contributing Factors

1. {Factor 1}
2. {Factor 2}

## Impact

- {X} companies affected
- {Y} API requests failed
- {Z} minutes of downtime

## What Went Well

- {observation 1}

## What Went Poorly

- {observation 1}

## Action Items

| Action | Owner | Due Date | Priority |
|--------|-------|----------|----------|
| {task} | {name} | {date} | P{N} |
```

---

## 7. On-Call Setup

### Required Tools

```bash
# Install on personal laptop:
brew install awscli    # AWS CLI for S3 backups
brew install docker    # Docker Desktop
brew install gh        # GitHub CLI

# Configure:
aws configure --profile madar-prod
ssh-copy-id -i ~/.ssh/madar_prod ubuntu@prod.madar.app

# Bookmark:
# - Grafana: https://grafana.internal:3001 (via SSH tunnel)
# - Sentry: https://sentry.io/organizations/madar/
# - GitHub Actions: https://github.com/mdardash-star/MADAR/actions
# - UptimeRobot: https://uptimerobot.com/dashboard
```

### On-Call Checklist (Start of Week)

- [ ] PagerDuty app installed and notifications enabled
- [ ] SSH access to production server tested
- [ ] Grafana dashboards loading correctly
- [ ] INCIDENT_RESPONSE.md read and bookmarked
- [ ] Escalation contacts saved in phone

---

## 8. Incident History Log

| Date | Severity | Title | Duration | RCA Link |
|------|----------|-------|----------|----------|
| 2026-07-18 | P2 | Docker network attachment failure | 15 min | RELEASE_VALIDATION.md |
| | | | | |
