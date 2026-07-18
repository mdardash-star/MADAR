# MADAR — Monitoring

**Version**: 1.0  
**Date**: 2026-07-18  
**Status**: Active  
**Owner**: DevOps Lead  

---

## 1. Monitoring Stack

| Tool | Role | Port | Access |
|------|------|------|--------|
| Prometheus | Metrics collection and storage | 9090 | Internal only |
| Grafana | Dashboards and visualization | 3001 | VPN / SSH tunnel |
| Loki | Log aggregation | 3100 | Internal only |
| Alertmanager | Alert routing | 9093 | Internal only |
| Sentry | Error tracking | Cloud SaaS | Web UI |
| UptimeRobot | External uptime monitoring | Cloud SaaS | Web UI |

---

## 2. Alert Severity Levels

| Level | Name | Response Time | Examples |
|-------|------|--------------|---------|
| P1 | **Critical** | Immediate (< 15 min) | Service down, data loss risk |
| P2 | **High** | 1 hour | Error rate > 5%, DB degraded |
| P3 | **Medium** | 4 hours | Performance degradation, high latency |
| P4 | **Low** | Next business day | Resource usage warnings |
| P5 | **Info** | No action required | Informational events |

---

## 3. Alert Rules

### P1 — Critical (PagerDuty + Slack)

```yaml
# infra/prometheus/rules/critical.yml
groups:
  - name: critical
    rules:
      - alert: ServiceDown
        expr: up{job="madar-api"} == 0
        for: 1m
        labels:
          severity: critical
          pager: "yes"
        annotations:
          summary: "MADAR API is DOWN"
          description: "The API service has been unreachable for > 1 minute"
          runbook: "https://github.com/mdardash-star/MADAR/blob/main/INCIDENT_RESPONSE.md#service-down"

      - alert: DatabaseDown
        expr: up{job="postgres"} == 0
        for: 1m
        labels:
          severity: critical
          pager: "yes"
        annotations:
          summary: "PostgreSQL database is DOWN"

      - alert: HighErrorRate
        expr: |
          rate(http_requests_total{status=~"5.."}[5m]) /
          rate(http_requests_total[5m]) > 0.05
        for: 2m
        labels:
          severity: critical
          pager: "yes"
        annotations:
          summary: "Error rate above 5% for 2+ minutes"
          description: "{{ $value | humanizePercentage }} of requests are failing"

      - alert: DiskAlmostFull
        expr: |
          (node_filesystem_avail_bytes / node_filesystem_size_bytes) < 0.1
        for: 5m
        labels:
          severity: critical
          pager: "yes"
        annotations:
          summary: "Disk less than 10% free"
```

### P2 — High (Slack + Email)

```yaml
      - alert: HighLatency
        expr: |
          histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) > 2.0
        for: 5m
        labels:
          severity: high
        annotations:
          summary: "p95 API response time > 2 seconds"

      - alert: HighCPU
        expr: |
          100 - (avg by(instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100) > 85
        for: 10m
        labels:
          severity: high
        annotations:
          summary: "CPU usage above 85% for 10+ minutes"

      - alert: HighMemory
        expr: |
          (1 - node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes) > 0.90
        for: 5m
        labels:
          severity: high
        annotations:
          summary: "Memory usage above 90%"

      - alert: DatabaseConnectionsHigh
        expr: |
          pg_stat_database_numbackends / pg_settings_max_connections > 0.80
        for: 5m
        labels:
          severity: high
        annotations:
          summary: "PostgreSQL connections above 80% of maximum"

      - alert: BackupFailed
        expr: time() - madar_backup_timestamp > 86400
        for: 1h
        labels:
          severity: high
        annotations:
          summary: "Daily database backup has not run in 24+ hours"
```

### P3 — Medium (Slack only)

```yaml
      - alert: SlowQueries
        expr: |
          rate(pg_stat_statements_mean_exec_time_seconds[5m]) > 1.0
        for: 10m
        labels:
          severity: medium
        annotations:
          summary: "Average database query time > 1 second"

      - alert: DiskGrowingFast
        expr: |
          predict_linear(node_filesystem_avail_bytes[4h], 24*3600) < 0
        for: 30m
        labels:
          severity: medium
        annotations:
          summary: "Disk predicted to be full within 24 hours"

      - alert: SslCertificateExpiringSoon
        expr: |
          probe_ssl_earliest_cert_expiry - time() < 14 * 24 * 3600
        for: 5m
        labels:
          severity: medium
        annotations:
          summary: "SSL certificate expires in less than 14 days"
```

---

## 4. Alertmanager Routing

```yaml
# infra/alertmanager/alertmanager.yml
global:
  resolve_timeout: 5m
  slack_api_url: "${SLACK_WEBHOOK_URL}"

route:
  group_by: ["alertname", "severity"]
  group_wait: 30s
  group_interval: 5m
  repeat_interval: 4h
  receiver: "slack-default"
  routes:
    - match:
        pager: "yes"
      receiver: "pagerduty-critical"
      continue: true
    - match:
        severity: "critical"
      receiver: "slack-critical"
    - match:
        severity: "high"
      receiver: "slack-high"
    - match:
        severity: "medium"
      receiver: "slack-medium"

receivers:
  - name: "pagerduty-critical"
    pagerduty_configs:
      - service_key: "${PAGERDUTY_SERVICE_KEY}"
        description: "{{ range .Alerts }}{{ .Annotations.summary }}\n{{ end }}"

  - name: "slack-critical"
    slack_configs:
      - channel: "#alerts-critical"
        title: "🚨 CRITICAL: {{ .CommonAnnotations.summary }}"
        text: "{{ range .Alerts }}{{ .Annotations.description }}\n{{ end }}"
        color: "danger"

  - name: "slack-high"
    slack_configs:
      - channel: "#alerts-high"
        title: "⚠️ HIGH: {{ .CommonAnnotations.summary }}"
        color: "warning"

  - name: "slack-medium"
    slack_configs:
      - channel: "#alerts-medium"
        title: "ℹ️ MEDIUM: {{ .CommonAnnotations.summary }}"
        color: "good"

  - name: "slack-default"
    slack_configs:
      - channel: "#alerts-all"
        title: "Alert: {{ .CommonAnnotations.summary }}"
```

---

## 5. External Monitoring (UptimeRobot)

Free tier provides 5-minute interval checks from external locations:

| Monitor | URL | Check Type | Alert If |
|---------|-----|------------|----------|
| API Health | `https://app.madar.app/health` | HTTP | Status != 200 |
| Frontend | `https://app.madar.app` | HTTP | Status != 200 |
| Login page | `https://app.madar.app/login` | HTTP | Status != 200 |
| SSL certificate | `https://app.madar.app` | SSL | Expiry < 7 days |

Alert channels: Email + Slack

---

## 6. Grafana Dashboard Panels

### SLA Dashboard

```
┌────────────────────────────────────────────────────────┐
│  MADAR SLA Dashboard                     Last 30 days  │
├──────────────┬─────────────┬─────────────┬────────────┤
│ Uptime       │ Error Rate  │ Avg Latency │ P95 Latency│
│ 99.97%       │ 0.02%       │ 12ms        │ 48ms       │
│ ✅ SLA MET   │ ✅ < 0.1%   │ ✅ < 50ms   │ ✅ < 200ms │
├──────────────┴─────────────┴─────────────┴────────────┤
│              Request Rate (req/s)                       │
│  ┌──────────────────────────────────────────────────┐  │
│  │  ▂▃▄▅▆▅▄▃▅▆▇▆▅▄▃▂▁▂▃▄▅▆▅▄▃▄▅▆▇▆▅▄▃▂▁▂▃▄▅▆       │  │
│  └──────────────────────────────────────────────────┘  │
├─────────────────────────────────────────────────────── ┤
│              Error Rate by Endpoint                     │
│  /auth/login      0.1%  ████░░░░░░░░░░░░░░░░░░       │  │
│  /master-data/*   0.0%  ░░░░░░░░░░░░░░░░░░░░░░       │  │
└────────────────────────────────────────────────────────┘
```

---

## 7. SLA Targets

| Tier | Uptime SLA | Planned Maintenance | Support Response |
|------|-----------|---------------------|-----------------|
| Starter | Best effort | Any time | N/A |
| Growth | 99.5% | < 4h/month | 48h email |
| Professional | 99.9% | < 1h/month | 24h email |
| Enterprise | 99.95% | Scheduled off-hours | 4h SLA |

### SLA Calculation

```
Uptime % = (Total minutes - Downtime minutes) / Total minutes × 100

Monthly uptime allowances:
99.9% = 44 minutes/month downtime allowed
99.5% = 3.6 hours/month downtime allowed
99.95% = 22 minutes/month downtime allowed
```

### SLA Credits

| Actual Uptime | Credit |
|---------------|--------|
| 99.0% - 99.9% | 10% of monthly fee |
| 98.0% - 99.0% | 25% of monthly fee |
| < 98.0% | 50% of monthly fee |

---

## 8. Monitoring Access

### Grafana

```bash
# Access via SSH tunnel (no public exposure)
ssh -L 3001:localhost:3001 ubuntu@prod.madar.app

# Browser: http://localhost:3001
# Default credentials: admin / (from .env.production)
```

### Prometheus

```bash
ssh -L 9090:localhost:9090 ubuntu@prod.madar.app
# Browser: http://localhost:9090
```

### On-Call Schedule

| Week | Primary | Secondary |
|------|---------|-----------|
| Week 1 | DevOps Lead | Backend Lead |
| Week 2 | Backend Lead | DevOps Lead |
| Week 3 | DevOps Lead | Backend Lead |
| (Rotate every 2 weeks) | | |

### PagerDuty Escalation

```
Triggered alert
    │ 5 min
    ▼
On-call engineer notified (push + SMS)
    │ 15 min (no acknowledge)
    ▼
Secondary on-call notified
    │ 30 min (no acknowledge)
    ▼
DevOps Lead + CTO notified
```
