# MADAR — Backup and Recovery

**Version**: 1.0  
**Date**: 2026-07-18  
**Status**: Active  
**Owner**: DevOps Lead  

---

## 1. Backup Philosophy

- **3-2-1 Rule**: 3 copies, 2 different media, 1 offsite
- **Automated**: No manual steps required for daily backups
- **Tested**: Recovery tested monthly; untested backups don't exist
- **Encrypted**: All backups encrypted at rest and in transit
- **Monitored**: Failed backups alert on-call immediately

---

## 2. Backup Schedule

| Type | Frequency | Time (UTC) | Retention | Storage |
|------|-----------|------------|-----------|---------|
| Full DB dump | Daily | 02:00 | 30 days | S3 + local |
| WAL archive | Continuous | Real-time | 7 days | S3 |
| Weekly snapshot | Sunday | 03:00 | 90 days | S3 |
| Monthly archive | 1st of month | 04:00 | 1 year | S3 Glacier |
| Config backup | On change | Immediate | Indefinite | Git |
| Application code | On commit | Immediate | Indefinite | GitHub |

---

## 3. Backup Scripts

### Daily Database Backup (`scripts/backup.sh`)

```bash
#!/bin/bash
set -euo pipefail

# Configuration
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_DIR="/opt/madar/backups"
BACKUP_FILE="${BACKUP_DIR}/madar_${TIMESTAMP}.sql.gz"
S3_BUCKET="${S3_BACKUP_BUCKET:-s3://madar-backups}"
RETENTION_DAYS=30
LOG_FILE="/var/log/madar/backup.log"

# Create backup directory
mkdir -p "${BACKUP_DIR}"
mkdir -p "$(dirname "${LOG_FILE}")"

log() { echo "[$(date -Iseconds)] $*" | tee -a "${LOG_FILE}"; }

log "Starting database backup..."

# Run pg_dump inside container
docker compose -f /opt/madar/docker-compose.prod.yml exec -T db \
  pg_dump -U "${POSTGRES_USER:-madar}" "${POSTGRES_DB:-madar_prod}" \
  | gzip -9 > "${BACKUP_FILE}"

BACKUP_SIZE=$(du -sh "${BACKUP_FILE}" | cut -f1)
log "Backup created: ${BACKUP_FILE} (${BACKUP_SIZE})"

# Verify backup integrity
gunzip -t "${BACKUP_FILE}" || {
  log "ERROR: Backup file is corrupted!"
  exit 1
}
log "Backup integrity verified"

# Upload to S3
aws s3 cp "${BACKUP_FILE}" "${S3_BUCKET}/daily/${TIMESTAMP}/" \
  --storage-class STANDARD_IA \
  --sse AES256 || {
  log "ERROR: Failed to upload to S3!"
  exit 1
}
log "Backup uploaded to S3"

# Remove local backups older than 3 days (S3 retains 30 days)
find "${BACKUP_DIR}" -name "*.sql.gz" -mtime +3 -delete
log "Old local backups cleaned up"

# Report success metrics to monitoring
curl -s -X POST "${PROMETHEUS_PUSHGATEWAY:-http://localhost:9091}/metrics/job/backup" \
  --data-binary "madar_backup_success{type=\"daily\"} 1
madar_backup_size_bytes{type=\"daily\"} $(stat -c%s "${BACKUP_FILE}")
madar_backup_timestamp{type=\"daily\"} $(date +%s)" 2>/dev/null || true

log "Daily backup completed successfully"
```

### Database Restore (`scripts/restore.sh`)

```bash
#!/bin/bash
set -euo pipefail

BACKUP_FILE="${1:-}"
LOG_FILE="/var/log/madar/restore.log"

log() { echo "[$(date -Iseconds)] $*" | tee -a "${LOG_FILE}"; }

if [[ -z "${BACKUP_FILE}" ]]; then
  echo "Usage: $0 <backup-file.sql.gz>"
  echo ""
  echo "Available backups:"
  ls -lt /opt/madar/backups/*.sql.gz 2>/dev/null | head -10
  echo ""
  echo "S3 backups:"
  aws s3 ls "${S3_BACKUP_BUCKET}/daily/" | sort -r | head -10
  exit 1
fi

log "WARNING: This will OVERWRITE the production database!"
read -p "Type 'CONFIRM' to proceed: " CONFIRM
[[ "${CONFIRM}" == "CONFIRM" ]] || { log "Restore cancelled"; exit 1; }

# If S3 path, download first
if [[ "${BACKUP_FILE}" == s3://* ]]; then
  LOCAL_FILE="/tmp/madar_restore_$(date +%s).sql.gz"
  log "Downloading from S3..."
  aws s3 cp "${BACKUP_FILE}" "${LOCAL_FILE}"
  BACKUP_FILE="${LOCAL_FILE}"
fi

# Verify backup integrity before restoring
log "Verifying backup integrity..."
gunzip -t "${BACKUP_FILE}" || { log "ERROR: Backup file is corrupted!"; exit 1; }

# Take a safety backup of current state before restoring
log "Taking safety backup of current state..."
SAFETY_BACKUP="/opt/madar/backups/pre-restore_$(date +%Y%m%d_%H%M%S).sql.gz"
docker compose -f /opt/madar/docker-compose.prod.yml exec -T db \
  pg_dump -U "${POSTGRES_USER:-madar}" "${POSTGRES_DB:-madar_prod}" \
  | gzip -9 > "${SAFETY_BACKUP}"
log "Safety backup: ${SAFETY_BACKUP}"

# Stop application to prevent writes during restore
log "Stopping application containers..."
docker compose -f /opt/madar/docker-compose.prod.yml stop api web

# Drop and recreate database
log "Recreating database..."
docker compose -f /opt/madar/docker-compose.prod.yml exec -T db psql \
  -U "${POSTGRES_USER:-madar}" -c \
  "DROP DATABASE IF EXISTS ${POSTGRES_DB:-madar_prod}; CREATE DATABASE ${POSTGRES_DB:-madar_prod};"

# Restore
log "Restoring backup..."
gunzip -c "${BACKUP_FILE}" | docker compose -f /opt/madar/docker-compose.prod.yml exec -T db \
  psql -U "${POSTGRES_USER:-madar}" "${POSTGRES_DB:-madar_prod}"

log "Restore completed"

# Restart application
log "Restarting application..."
docker compose -f /opt/madar/docker-compose.prod.yml start api web

# Verify application health
sleep 10
curl -f http://localhost:8000/health || {
  log "ERROR: Application health check failed after restore!"
  log "Rollback by restoring: ${SAFETY_BACKUP}"
  exit 1
}

log "Application healthy after restore. Restore completed successfully."
```

---

## 4. Point-in-Time Recovery (PITR)

### WAL Archiving Setup

```bash
# postgresql.conf
wal_level = replica
archive_mode = on
archive_command = 'aws s3 cp %p s3://madar-backups/wal/%f'
archive_timeout = 300  # Archive every 5 minutes at minimum

# Recovery to specific timestamp:
# 1. Restore base backup
# 2. Create recovery.conf
restore_command = 'aws s3 cp s3://madar-backups/wal/%f %p'
recovery_target_time = '2026-07-18 14:30:00'
recovery_target_action = 'promote'
```

---

## 5. Recovery Runbooks

### Scenario 1: Accidental Data Deletion

```bash
# 1. Identify when deletion occurred (from audit_logs)
docker compose exec db psql -U madar -c \
  "SELECT * FROM audit_logs WHERE action='delete' ORDER BY created_at DESC LIMIT 20;"

# 2. Get the most recent backup before deletion
aws s3 ls s3://madar-backups/daily/ | sort -r | head -5

# 3. Restore to temporary database
docker compose exec db createdb -U madar madar_recovery
gunzip -c /path/to/backup.sql.gz | docker compose exec -T db psql -U madar madar_recovery

# 4. Extract deleted records
docker compose exec db psql -U madar -c \
  "INSERT INTO madar_prod.customers SELECT * FROM madar_recovery.customers WHERE id IN (1,2,3);"

# 5. Drop temporary database
docker compose exec db dropdb -U madar madar_recovery
```

### Scenario 2: Complete Database Corruption

```bash
# 1. Take the application offline
docker compose -f docker-compose.prod.yml stop api web

# 2. Identify latest clean backup
aws s3 ls s3://madar-backups/daily/ | sort -r | head -3

# 3. Execute restore
bash scripts/restore.sh s3://madar-backups/daily/latest/madar_YYYYMMDD.sql.gz

# 4. Verify data integrity
docker compose exec api python -c "from app.core.database import engine; print(engine.execute('SELECT count(*) FROM companies').scalar(), 'companies found')"

# 5. Run any pending migrations
docker compose exec api alembic upgrade head

# 6. Restart and monitor
docker compose -f docker-compose.prod.yml start api web
```

### Scenario 3: Server Complete Failure

```bash
# On new server:

# 1. Provision new server with same spec
# 2. Install Docker + Docker Compose
# 3. Clone repository
git clone https://github.com/mdardash-star/MADAR.git /opt/madar
cd /opt/madar

# 4. Copy secrets from secure storage (LastPass, Vault, etc.)
cp .env.production.secure .env.production

# 5. Start stack (will fail on migrations, that's ok)
docker compose -f docker-compose.prod.yml up -d db redis nginx
sleep 30

# 6. Restore latest backup
aws s3 cp s3://madar-backups/daily/latest/ /opt/madar/backups/ --recursive
bash scripts/restore.sh /opt/madar/backups/madar_latest.sql.gz

# 7. Start application
docker compose -f docker-compose.prod.yml up -d api web

# 8. Update DNS to point to new server IP
# Cloudflare: update A record for app.madar.app
```

---

## 6. Backup Verification Testing

### Monthly Recovery Test

Run on the **first Tuesday of each month** in staging environment:

```bash
#!/bin/bash
# scripts/test-restore.sh
# Verify backup can be restored successfully

LATEST_BACKUP=$(aws s3 ls s3://madar-backups/daily/ | sort -r | head -1 | awk '{print $4}')
aws s3 cp "s3://madar-backups/daily/${LATEST_BACKUP}" /tmp/

# Restore to isolated test container
docker run --rm -d --name madar-restore-test \
  -e POSTGRES_DB=madar_test \
  -e POSTGRES_USER=madar \
  -e POSTGRES_PASSWORD=test123 \
  postgres:16-alpine

sleep 5

gunzip -c /tmp/${LATEST_BACKUP} | docker exec -i madar-restore-test \
  psql -U madar -d madar_test

# Verify table counts
COMPANY_COUNT=$(docker exec madar-restore-test psql -U madar -d madar_test -t -c \
  "SELECT count(*) FROM companies WHERE is_deleted=false;")

if [[ "${COMPANY_COUNT}" -gt "0" ]]; then
  echo "✅ Restore test PASSED: ${COMPANY_COUNT} companies found"
else
  echo "❌ Restore test FAILED: no companies found"
  exit 1
fi

docker stop madar-restore-test
rm /tmp/${LATEST_BACKUP}
```

---

## 7. S3 Lifecycle Policy

```json
{
  "Rules": [
    {
      "Id": "DailyBackupLifecycle",
      "Filter": { "Prefix": "daily/" },
      "Status": "Enabled",
      "Transitions": [
        { "Days": 30, "StorageClass": "STANDARD_IA" },
        { "Days": 90, "StorageClass": "GLACIER" }
      ],
      "Expiration": { "Days": 365 }
    },
    {
      "Id": "WALLifecycle",
      "Filter": { "Prefix": "wal/" },
      "Status": "Enabled",
      "Expiration": { "Days": 7 }
    }
  ]
}
```

---

## 8. Monitoring Backup Health

```yaml
# Grafana alert: backup failed
- alert: BackupFailed
  expr: time() - madar_backup_timestamp{type="daily"} > 86400
  for: 1h
  labels:
    severity: critical
  annotations:
    summary: "Daily database backup has not run in 24+ hours"
    runbook: "https://github.com/mdardash-star/MADAR/BACKUP_AND_RECOVERY.md"

# Grafana alert: backup size anomaly
- alert: BackupSizeAnomaly
  expr: |
    madar_backup_size_bytes > 
    avg_over_time(madar_backup_size_bytes[7d]) * 2
  for: 5m
  labels:
    severity: warning
  annotations:
    summary: "Backup size is 2x larger than 7-day average — unexpected data growth"
```

---

## 9. RTO and RPO Targets

| Scenario | RTO Target | RPO Target | Method |
|----------|-----------|-----------|--------|
| Container restart | < 1 min | 0 | Auto-restart |
| DB connection loss | < 2 min | 0 | Connection retry |
| Accidental deletion (row) | < 30 min | < 24h | Restore from daily backup |
| Database corruption | < 2 hours | < 24h | Full restore from daily backup |
| Server failure | < 4 hours | < 24h | New server + restore |
| Complete datacenter loss | < 24 hours | < 24h | S3 backup to new region |

---

## 10. Contact and Escalation

| Issue | First Responder | Escalation |
|-------|----------------|------------|
| Backup failed (monitoring alert) | DevOps on-call | DevOps Lead within 1h |
| Restore needed | DevOps Lead | CTO if > 2h |
| Data loss suspected | CTO + DevOps Lead | Legal/compliance team |
