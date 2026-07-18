# MADAR — Deployment Plan

**Version**: 1.0  
**Date**: 2026-07-18  
**Status**: Active  
**Owner**: DevOps Lead  

---

## 1. Deployment Philosophy

MADAR follows a **progressive deployment strategy**:

```
Local Dev → Staging → Production
     ↓           ↓          ↓
  Docker     Docker     Cloud VM / Kubernetes
  Compose    Compose    (single-node → multi-node)
```

**Principles:**
- Immutable infrastructure — containers rebuilt from source, never patched in place
- Blue/Green deployments for zero-downtime updates
- Automated smoke tests before traffic cutover
- Rollback in < 5 minutes

---

## 2. Environments

| Environment | Purpose | URL | Branch | Deploy Trigger |
|-------------|---------|-----|--------|----------------|
| **local** | Developer sandbox | localhost:3000 | any | manual |
| **staging** | Integration + QA | staging.madar.app | develop | push to `develop` |
| **production** | Live customers | app.madar.app | main | manual approval after CI |

### Environment Variables per Tier

| Variable | local | staging | production |
|----------|-------|---------|------------|
| `DEBUG` | true | false | false |
| `APP_ENV` | development | staging | production |
| `JWT_SECRET_KEY` | dev-secret | Secrets Manager | Secrets Manager |
| `POSTGRES_PASSWORD` | dev-password | Random 32-char | Random 32-char |
| `LOG_LEVEL` | DEBUG | INFO | WARNING |
| `CORS_ORIGINS` | * | staging.madar.app | app.madar.app |

---

## 3. Infrastructure Requirements

### Minimum Production Server

| Component | Spec | Notes |
|-----------|------|-------|
| CPU | 4 vCPU | 2 for API, 2 for DB |
| RAM | 8 GB | 2G API, 4G Postgres, 2G OS/cache |
| Storage | 100 GB SSD | 20G app, 80G DB |
| OS | Ubuntu 24.04 LTS | LTS for 5-year support |
| Network | 1 Gbps | Standard cloud VM |

### Recommended Production Architecture (Phase 1)

```
Internet
   │
   ▼
[Cloudflare CDN + DDoS Protection]
   │
   ▼
[Nginx Reverse Proxy + TLS termination]
   │
   ├─── /api/* ──► [FastAPI Uvicorn workers ×2]
   │                      │
   └─── /* ─────► [Next.js Node.js]   [PostgreSQL 16]
                                       [Redis 7]
```

### Phase 2 (Scale-Out)

```
[Load Balancer]
   ├── API instance 1
   ├── API instance 2
   └── API instance N
         │
    [PgBouncer connection pooler]
         │
    [PostgreSQL primary + 1 replica]
         │
    [Redis Sentinel / Redis Cluster]
```

---

## 4. Deployment Procedure

### Initial Production Deployment

```bash
# 1. Provision server
ssh ubuntu@prod.madar.app

# 2. Install Docker
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker ubuntu

# 3. Clone repository
git clone https://github.com/mdardash-star/MADAR.git /opt/madar
cd /opt/madar

# 4. Configure secrets
cp .env.production.example .env.production
# Edit .env.production with production values
# Use: openssl rand -hex 32 for JWT_SECRET_KEY

# 5. Start production stack
docker compose -f docker-compose.prod.yml up -d

# 6. Run migrations
docker compose -f docker-compose.prod.yml exec api alembic upgrade head

# 7. Verify
curl -f https://app.madar.app/health
```

### Zero-Downtime Update Procedure

```bash
# On production server:
cd /opt/madar

# 1. Pull latest code
git pull origin main

# 2. Build new images
docker compose -f docker-compose.prod.yml build

# 3. Rolling restart (API first, then web)
docker compose -f docker-compose.prod.yml up -d --no-deps --build api
sleep 10
curl -f http://localhost:8000/health || (echo "ROLLBACK" && docker compose -f docker-compose.prod.yml rollout api && exit 1)

docker compose -f docker-compose.prod.yml up -d --no-deps --build web

# 4. Run migrations if needed
docker compose -f docker-compose.prod.yml exec api alembic upgrade head

# 5. Smoke test
make smoke-test ENV=production
```

### Rollback Procedure

```bash
# Immediate rollback to previous image
docker compose -f docker-compose.prod.yml rollout api
docker compose -f docker-compose.prod.yml rollout web

# Rollback to specific git tag
git checkout v1.0.0-rc1
docker compose -f docker-compose.prod.yml up -d --build

# Database rollback (if migration was applied)
docker compose -f docker-compose.prod.yml exec api alembic downgrade -1
```

---

## 5. Pre-Deployment Checklist

### Code Checks (CI enforced)
- [ ] All tests pass (49+ automated tests)
- [ ] No lint errors (`ruff check .`)
- [ ] TypeScript build clean (0 errors)
- [ ] No secrets committed to git
- [ ] RELEASE_VALIDATION.md updated

### Infrastructure Checks
- [ ] SSL certificate valid (< 60 days to expiry → renew)
- [ ] Database backup completed within 24h
- [ ] Disk space > 20% free
- [ ] Memory < 80% utilization
- [ ] All health checks passing

### Security Checks
- [ ] `JWT_SECRET_KEY` is not the default value
- [ ] `POSTGRES_PASSWORD` is strong and unique
- [ ] API docs (`/docs`, `/redoc`) disabled in production
- [ ] CORS origins restricted to production domain
- [ ] All `npm audit` high/critical vulnerabilities resolved

### Post-Deployment Checks
- [ ] `GET /health` returns 200
- [ ] Login flow works end-to-end
- [ ] Dashboard loads with correct data
- [ ] Error rate < 0.1% (check Grafana)
- [ ] Response times within baseline (check Grafana)
- [ ] No new errors in Loki logs

---

## 6. Cloud Provider Options

### Option A: DigitalOcean (Recommended for early stage)
- **Droplet**: $48/month (4 vCPU, 8 GB RAM)
- **Managed Postgres**: $50/month (2 vCPU, 4 GB)
- **Spaces (S3 backup)**: $5/month
- **Total**: ~$103/month
- **Pros**: Simple, affordable, good SLA

### Option B: AWS (Enterprise-ready)
- **EC2 t3.large**: $60/month
- **RDS Postgres db.t3.medium**: $65/month
- **S3 backup**: $5/month
- **CloudFront CDN**: ~$10/month
- **Total**: ~$140/month
- **Pros**: Mature ecosystem, compliance certs (SOC2, ISO27001)

### Option C: Azure (MENA-region optimized)
- **Standard_D2s_v3**: $70/month
- **Azure Database for PostgreSQL**: $80/month
- **Blob Storage**: $5/month
- **Total**: ~$155/month
- **Pros**: Azure UAE North region (low latency for MENA)

---

## 7. Domain and SSL Configuration

```
# Primary domain
app.madar.app          → Production frontend
api.madar.app          → Production API (optional split)
staging.madar.app      → Staging frontend

# SSL: Let's Encrypt (Certbot) — auto-renewed
certbot certonly --webroot -w /var/www/certbot \
  -d app.madar.app \
  -d api.madar.app \
  --agree-tos --email ops@madar.app

# Auto-renewal via cron (runs twice daily)
0 */12 * * * certbot renew --quiet --deploy-hook "docker compose -f /opt/madar/docker-compose.prod.yml restart nginx"
```

---

## 8. Deployment Timeline

| Phase | Target Date | Activities |
|-------|-------------|-----------|
| **Infrastructure Setup** | Week 1 | Provision server, DNS, SSL, Docker |
| **Staging Deploy** | Week 1 | Deploy to staging, smoke tests |
| **Load Testing** | Week 2 | k6 load tests, bottleneck identification |
| **Security Audit** | Week 2 | External pen test, vulnerability scan |
| **Production Deploy** | Week 3 | Go-live with monitoring |
| **Hypercare** | Weeks 3-4 | 24/7 monitoring, rapid response |
| **Steady State** | Week 5+ | Normal operations |
