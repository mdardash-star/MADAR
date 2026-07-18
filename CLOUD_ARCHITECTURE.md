# MADAR — Cloud Architecture

**Version**: 1.0  
**Date**: 2026-07-18  
**Status**: Active  
**Owner**: CTO / DevOps Lead  

---

## 1. Architecture Overview

### Phase 1 — Single-Region, Single-Node (Launch)

```
┌─────────────────────────────────────────────────────────────┐
│                      Cloudflare (CDN + WAF + DDoS)          │
└─────────────────────────────┬───────────────────────────────┘
                              │ HTTPS :443
┌─────────────────────────────▼───────────────────────────────┐
│                    Production Server (Ubuntu 24.04)         │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │               Nginx (Reverse Proxy)                  │   │
│  │  :80 → redirect :443  |  :443 → TLS termination     │   │
│  └────────────┬────────────────────────┬───────────────┘   │
│               │                        │                    │
│  ┌────────────▼──────┐    ┌───────────▼────────────────┐  │
│  │   Next.js :3000   │    │   FastAPI/Uvicorn :8000     │  │
│  │   (Web Frontend)  │    │   (REST API, 2 workers)     │  │
│  └───────────────────┘    └──────────┬─────────────────┘  │
│                                       │                     │
│  ┌────────────────────────────────────▼─────────────────┐  │
│  │           Internal Docker Network (madar_prod)        │  │
│  │                                                       │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌────────────┐ │  │
│  │  │ PostgreSQL 16│  │  Redis 7     │  │  Nginx     │ │  │
│  │  │ :5432 (int)  │  │  :6379 (int) │  │  Certbot   │ │  │
│  │  └──────────────┘  └──────────────┘  └────────────┘ │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                             │
│  ┌────────────────────────────────────────────────────────┐ │
│  │           Observability Stack (internal)               │ │
│  │  Prometheus :9090 | Grafana :3001 | Loki :3100        │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
              │ SSH :22 (restricted to admin IPs)
              │ Postgres :5432 CLOSED to internet
              │ Redis :6379 CLOSED to internet
```

### Phase 2 — Multi-AZ (6 months post-launch)

```
┌─────────────────────────────────────────────────────────────┐
│                      Cloudflare (CDN + WAF)                 │
└──────────────────────────────┬──────────────────────────────┘
                               │
                    ┌──────────▼──────────┐
                    │  Cloud Load Balancer │
                    └──────┬──────────────┘
                    ┌──────┴──────────────┐
               ┌────▼────┐          ┌────▼────┐
               │ Node 1  │          │ Node 2  │
               │ AZ-1    │          │ AZ-2    │
               └────┬────┘          └────┬────┘
                    └──────┬─────────────┘
                    ┌──────▼──────────┐
                    │   PgBouncer     │ ← connection pooler
                    └──────┬──────────┘
               ┌───────────┴─────────────┐
          ┌────▼────┐              ┌─────▼────┐
          │ PG Prim │ ──streaming──► PG Repl  │
          │ AZ-1    │              │ AZ-2     │
          └─────────┘              └──────────┘
```

### Phase 3 — Kubernetes (12+ months, enterprise scale)

```
EKS / GKE / AKS Cluster
├── Ingress Controller (Nginx/Traefik)
├── API Deployment (HPA: 2-10 pods)
├── Web Deployment (HPA: 2-5 pods)
├── Background Workers (Celery/RQ)
├── CronJobs (backups, data cleanup)
└── Monitoring Namespace
    ├── Prometheus Operator
    ├── Grafana
    └── Loki
```

---

## 2. Container Architecture

### Service Map

| Service | Image | Port (internal) | Port (external) | HA Strategy |
|---------|-------|-----------------|-----------------|-------------|
| `nginx` | nginx:alpine | 80, 443 | 80, 443 | Single (Phase 1) |
| `api` | madar-api | 8000 | via nginx | 2 workers (Phase 1) |
| `web` | madar-web | 3000 | via nginx | Single (Phase 1) |
| `db` | postgres:16-alpine | 5432 | closed | Primary + replica (Phase 2) |
| `redis` | redis:7-alpine | 6379 | closed | Sentinel (Phase 2) |
| `prometheus` | prom/prometheus | 9090 | internal | Single |
| `grafana` | grafana/grafana | 3001 | tunneled | Single |
| `loki` | grafana/loki | 3100 | internal | Single |
| `alertmanager` | prom/alertmanager | 9093 | internal | Single |

### Network Segmentation

```yaml
# Three Docker networks for security isolation
networks:
  frontend:        # nginx ↔ web, nginx ↔ api
  backend:         # api ↔ db, api ↔ redis
  observability:   # prometheus ↔ api, grafana ↔ prometheus
```

---

## 3. Data Architecture

### PostgreSQL Schema Strategy

```
Production Database: madar_prod
├── Schema: public (core application tables)
│   ├── companies      — tenant registry
│   ├── users          — per-tenant users
│   ├── branches       — per-tenant locations
│   ├── products       — per-tenant catalog
│   └── ... (40+ tables)
│
├── Schema: audit      — immutable audit trail
│   └── audit_logs     — all mutations logged
│
└── Schema: analytics  — read-only materialized views (Phase 2)
    ├── mv_daily_revenue
    └── mv_company_kpis
```

### Multi-Tenancy Data Isolation

```sql
-- All tenant tables have company_id column
-- Row-level filter enforced at application layer
-- Future: PostgreSQL Row Level Security (RLS)

ALTER TABLE companies ENABLE ROW LEVEL SECURITY;
CREATE POLICY tenant_isolation ON companies
  USING (id = current_setting('app.company_id')::int);
```

### Redis Usage

| Key Pattern | TTL | Purpose |
|-------------|-----|---------|
| `session:{token_hash}` | 60 min | JWT blacklist (revoked tokens) |
| `rate:{ip}:{endpoint}` | 1 min | Rate limit counters |
| `cache:dashboard:{company_id}` | 30 sec | Dashboard KPI cache |
| `lock:migration` | 60 sec | DB migration distributed lock |

---

## 4. Security Architecture

### Defense in Depth

```
Layer 1: Cloudflare WAF           — DDoS, bot mitigation, geo-blocking
Layer 2: Nginx                    — Rate limiting, security headers, TLS 1.2+
Layer 3: FastAPI middleware       — JWT validation, CORS, request size limits
Layer 4: Application (Pydantic)   — Input validation, type enforcement
Layer 5: Database (SQLAlchemy)    — Parameterized queries, ORM
Layer 6: PostgreSQL               — Row-level isolation, connection limits
```

### Secret Rotation Schedule

| Secret | Rotation Frequency | Method |
|--------|-------------------|--------|
| JWT_SECRET_KEY | Quarterly | Zero-downtime: dual-accept period |
| POSTGRES_PASSWORD | Quarterly | Maintenance window |
| SSL certificates | 90 days (auto) | Certbot auto-renew |
| Redis password | Quarterly | Maintenance window |
| Admin API keys | On demand | Immediate invalidation |

---

## 5. CDN and Static Assets

```
# Cloudflare configuration
DNS: app.madar.app → Production IP (Proxied)

Cache Rules:
- /static/* → Cache 30 days
- /_next/static/* → Cache 1 year (immutable)
- /api/* → Bypass cache
- /health → Bypass cache

# Next.js Static Export (optional Phase 2)
# Move to Cloudflare Pages for free CDN + global edge
```

---

## 6. Disaster Recovery Architecture

| Scenario | RTO | RPO | Recovery Method |
|----------|-----|-----|-----------------|
| Container crash | < 1 min | 0 | Docker restart policy |
| Server reboot | < 5 min | 0 | Docker Compose auto-start |
| Disk failure | < 1 hour | < 24h | Restore from S3 backup |
| Data corruption | < 4 hours | < 24h | Point-in-time restore |
| Server failure | < 2 hours | < 24h | New server + restore |
| Region failure | < 24 hours | < 24h | Manual failover to Phase 2 |

**RTO** = Recovery Time Objective (time to restore service)  
**RPO** = Recovery Point Objective (maximum data loss)

---

## 7. Cost Optimization

### Phase 1 Target: $103-155/month

| Resource | Cost Strategy |
|----------|--------------|
| Compute | Start with 1 server; scale when p95 API > 500ms |
| Database | Managed service for backups + failover automation |
| Storage | S3-compatible (Spaces/Wasabi) — $5/month for 100GB |
| CDN | Cloudflare free tier (unlimited bandwidth) |
| Monitoring | Self-hosted (Prometheus/Grafana) — $0 additional |
| SSL | Let's Encrypt — $0 |

### Phase 2 Target: $400-600/month
- Add replica DB, second app node, load balancer
- Enable auto-scaling based on CPU/memory metrics
