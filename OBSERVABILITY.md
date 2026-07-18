# MADAR — Observability Strategy

**Version**: 1.0  
**Date**: 2026-07-18  
**Status**: Active  
**Owner**: DevOps Lead  

---

## 1. Observability Pillars

MADAR implements the three pillars of observability:

```
┌─────────────────────────────────────────────────┐
│                  Observability                   │
│                                                  │
│  ┌──────────┐  ┌──────────┐  ┌──────────────┐  │
│  │  METRICS │  │   LOGS   │  │   TRACES     │  │
│  │          │  │          │  │              │  │
│  │Prometheus│  │   Loki   │  │  OpenTelemetry│  │
│  │ Grafana  │  │ Grafana  │  │  (Phase 2)   │  │
│  └──────────┘  └──────────┘  └──────────────┘  │
│                      │                          │
│              ┌───────▼────────┐                 │
│              │    Grafana     │                 │
│              │  (Unified UI)  │                 │
│              └───────────────┘                  │
│                                                  │
│  ┌──────────────────────────────────────────┐   │
│  │           ALERTING                        │  │
│  │  AlertManager → Slack / PagerDuty / Email │  │
│  └──────────────────────────────────────────┘   │
└─────────────────────────────────────────────────┘
```

---

## 2. Metrics (Prometheus)

### What to Measure

#### Application Metrics (via FastAPI instrumentation)

| Metric | Type | Labels | Description |
|--------|------|--------|-------------|
| `http_requests_total` | Counter | method, endpoint, status | Total HTTP requests |
| `http_request_duration_seconds` | Histogram | method, endpoint | Request latency |
| `http_requests_in_flight` | Gauge | endpoint | Concurrent requests |
| `db_query_duration_seconds` | Histogram | query_type | Database query time |
| `auth_login_attempts_total` | Counter | status (success/failed) | Auth events |
| `tenants_active_total` | Gauge | — | Active company count |
| `background_job_duration_seconds` | Histogram | job_name | Background task timing |

#### Business Metrics

| Metric | Type | Description |
|--------|------|-------------|
| `madar_companies_total` | Gauge | Total registered companies |
| `madar_users_total` | Gauge | Total active users |
| `madar_transactions_total` | Counter | Quotations + orders + invoices |
| `madar_api_calls_per_tenant` | Counter | API calls by company_id |

#### Infrastructure Metrics (node_exporter)

| Metric | Alert Threshold |
|--------|----------------|
| CPU usage | > 80% for 5min |
| Memory usage | > 85% |
| Disk usage | > 80% |
| Network errors | > 0 |
| Open file descriptors | > 80% of limit |

#### Database Metrics (postgres_exporter)

| Metric | Alert Threshold |
|--------|----------------|
| Active connections | > 80% of max_connections |
| Cache hit ratio | < 95% |
| Deadlocks/min | > 0 |
| Replication lag | > 5 seconds |
| Slow queries | > 5 queries/min over 1s |
| Autovacuum activity | Blocking queries |

### Prometheus Configuration

```yaml
# infra/prometheus/prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

rule_files:
  - "rules/*.yml"

alerting:
  alertmanagers:
    - static_configs:
        - targets: ["alertmanager:9093"]

scrape_configs:
  - job_name: "madar-api"
    static_configs:
      - targets: ["api:8000"]
    metrics_path: "/metrics"

  - job_name: "postgres"
    static_configs:
      - targets: ["postgres-exporter:9187"]

  - job_name: "redis"
    static_configs:
      - targets: ["redis-exporter:9121"]

  - job_name: "node"
    static_configs:
      - targets: ["node-exporter:9100"]

  - job_name: "nginx"
    static_configs:
      - targets: ["nginx-exporter:9113"]
```

---

## 3. Logs (Loki + Promtail)

### Log Format

All application logs use **structured JSON** format:

```json
{
  "timestamp": "2026-07-18T14:32:00.000Z",
  "level": "INFO",
  "logger": "madar.api",
  "message": "Request completed",
  "request_id": "req-abc123",
  "method": "GET",
  "path": "/api/v1/master-data/customers",
  "status_code": 200,
  "duration_ms": 4.2,
  "company_id": 42,
  "user_id": 7,
  "ip": "203.0.113.1"
}
```

### Log Levels

| Level | When | Volume |
|-------|------|--------|
| `DEBUG` | Local dev only | Very high |
| `INFO` | Request lifecycle, key events | Medium |
| `WARNING` | Unexpected but handled | Low |
| `ERROR` | Exceptions, failures | Very low |
| `CRITICAL` | System-level failures | Near zero |

### Log Categories

```python
# Different loggers for different concerns
import structlog

# Request logger — every HTTP request
request_log = structlog.get_logger("madar.request")

# Auth logger — security-relevant events
auth_log = structlog.get_logger("madar.auth")

# Business logger — key business events
business_log = structlog.get_logger("madar.business")

# DB logger — slow query logging
db_log = structlog.get_logger("madar.db")
```

### Loki Configuration

```yaml
# infra/loki/loki-config.yml
auth_enabled: false

server:
  http_listen_port: 3100

ingester:
  lifecycler:
    ring:
      kvstore:
        store: inmemory
      replication_factor: 1

schema_config:
  configs:
    - from: 2026-01-01
      store: boltdb-shipper
      object_store: filesystem
      schema: v11
      index:
        prefix: index_
        period: 24h

storage_config:
  boltdb_shipper:
    active_index_directory: /loki/index
    cache_location: /loki/index_cache
    shared_store: filesystem
  filesystem:
    directory: /loki/chunks

limits_config:
  retention_period: 744h  # 31 days
```

### Promtail Configuration (log shipper)

```yaml
# infra/promtail/promtail-config.yml
server:
  http_listen_port: 9080

clients:
  - url: http://loki:3100/loki/api/v1/push

scrape_configs:
  - job_name: madar-api
    static_configs:
      - targets:
          - localhost
        labels:
          job: madar-api
          __path__: /var/lib/docker/containers/*/*-json.log
    pipeline_stages:
      - docker: {}
      - json:
          expressions:
            level: level
            request_id: request_id
            company_id: company_id
      - labels:
          level:
          company_id:
```

---

## 4. Traces (OpenTelemetry — Phase 2)

### Planned Tracing Architecture

```
Request → FastAPI → OpenTelemetry SDK → OTLP Exporter
                                              │
                                        Jaeger / Tempo
                                              │
                                          Grafana UI
```

### Trace Context Propagation

```python
# Phase 2 implementation plan:
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor

# Auto-instrument all SQL queries
SQLAlchemyInstrumentor().instrument(engine=engine)

# Auto-instrument all HTTP handlers
FastAPIInstrumentor.instrument_app(app)

# Custom spans for business operations
tracer = trace.get_tracer("madar.business")

with tracer.start_as_current_span("create_invoice") as span:
    span.set_attribute("company_id", company_id)
    span.set_attribute("customer_id", customer_id)
    # ... business logic
```

---

## 5. Grafana Dashboards

### Dashboard 1: Application Health

Panels:
- Request rate (req/s) per endpoint
- Error rate (%) per endpoint
- p50/p95/p99 latency per endpoint
- Active connections
- Memory and CPU usage

### Dashboard 2: Business Intelligence

Panels:
- New company registrations (daily/weekly/monthly)
- Active companies (last 30 days)
- Transaction volume (quotations + orders + invoices)
- API calls per tenant
- Revenue proxy metrics (transactions × estimated value)

### Dashboard 3: Infrastructure

Panels:
- Server CPU/Memory/Disk
- Network I/O
- Docker container stats
- Database connection pool usage
- Redis memory and hit rate
- Nginx request throughput and error rate

### Dashboard 4: Security

Panels:
- Failed login attempts (rate, by IP)
- 401/403 response rate
- Rate-limit trigger frequency
- Unusual tenant API usage (anomaly detection)

---

## 6. Error Tracking (Sentry)

### Integration

```python
# apps/api/app/main.py
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration

sentry_sdk.init(
    dsn=settings.sentry_dsn,
    environment=settings.app_env,
    release=settings.api_version,
    integrations=[
        FastApiIntegration(transaction_style="endpoint"),
        SqlalchemyIntegration(),
    ],
    traces_sample_rate=0.1,       # 10% of requests traced
    profiles_sample_rate=0.1,     # 10% profiled
    send_default_pii=False,       # GDPR compliance
)
```

### Sentry Alert Rules

| Alert | Condition | Action |
|-------|-----------|--------|
| New error type | First occurrence | Slack #dev-alerts |
| Error spike | > 10x baseline in 1h | PagerDuty P2 |
| High error volume | > 1% of requests | PagerDuty P1 |
| Performance regression | p95 > 2x baseline | Slack #dev-alerts |

---

## 7. Health Checks

### `/health` (public, no auth)
```json
{ "status": "healthy" }
```

### `/health/ready` (readiness — for load balancer)
```json
{
  "status": "ready",
  "database": "connected",
  "redis": "connected",
  "migrations": "current"
}
```

### `/health/live` (liveness — for container orchestration)
```json
{
  "status": "alive",
  "uptime_seconds": 86400,
  "version": "1.0.0-rc1"
}
```

### `/metrics` (Prometheus scrape endpoint)
```
# HELP http_requests_total Total HTTP requests
# TYPE http_requests_total counter
http_requests_total{method="GET",endpoint="/api/v1/me",status="200"} 1423.0
...
```

---

## 8. On-Call Runbooks Reference

| Alert | Runbook |
|-------|---------|
| High error rate | See `INCIDENT_RESPONSE.md` — Section 4 |
| Database down | See `INCIDENT_RESPONSE.md` — Section 5 |
| High latency | See `PERFORMANCE_BASELINE.md` — Section 8 |
| Disk space low | See `BACKUP_AND_RECOVERY.md` — Section 5 |
| Backup failed | See `BACKUP_AND_RECOVERY.md` — Section 8 |
| Certificate expiry | See `DEPLOYMENT_PLAN.md` — Section 7 |
