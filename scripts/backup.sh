#!/usr/bin/env bash
# ============================================================
# MADAR Database Backup Script
# ============================================================
# Usage:
#   ./scripts/backup.sh                   # Uses production docker-compose
#   COMPOSE_FILE=docker-compose.yml ./scripts/backup.sh  # Override compose file
#
# Environment variables (read from shell or .env.production):
#   POSTGRES_USER, POSTGRES_DB, POSTGRES_PASSWORD
#   S3_BACKUP_BUCKET  (e.g., s3://madar-backups)
#   AWS_PROFILE       (optional, for named AWS profile)

set -euo pipefail

# ─── Config ──────────────────────────────────────────────────────────────────
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "${SCRIPT_DIR}")"
BACKUP_DIR="${PROJECT_DIR}/backups"
COMPOSE_FILE="${COMPOSE_FILE:-${PROJECT_DIR}/docker-compose.prod.yml}"
BACKUP_FILE="${BACKUP_DIR}/madar_${TIMESTAMP}.sql.gz"
S3_BUCKET="${S3_BACKUP_BUCKET:-}"
RETENTION_DAYS_LOCAL="${BACKUP_RETENTION_LOCAL:-3}"
LOG_FILE="/var/log/madar/backup.log"
PUSHGATEWAY_URL="${PROMETHEUS_PUSHGATEWAY_URL:-}"

# ─── Setup ───────────────────────────────────────────────────────────────────
mkdir -p "${BACKUP_DIR}"
mkdir -p "$(dirname "${LOG_FILE}" 2>/dev/null)" 2>/dev/null || true

log() {
    local msg="[$(date -Iseconds)] $*"
    echo "${msg}"
    echo "${msg}" >> "${LOG_FILE}" 2>/dev/null || true
}

die() {
    log "ERROR: $*"
    # Report failure to Prometheus pushgateway
    if [[ -n "${PUSHGATEWAY_URL}" ]]; then
        curl -s -X POST "${PUSHGATEWAY_URL}/metrics/job/madar_backup" \
            --data-binary "madar_backup_success 0" 2>/dev/null || true
    fi
    exit 1
}

# ─── Pre-flight checks ───────────────────────────────────────────────────────
log "Starting MADAR database backup..."
log "  Compose file: ${COMPOSE_FILE}"
log "  Backup path:  ${BACKUP_FILE}"

[[ -f "${COMPOSE_FILE}" ]] || die "Compose file not found: ${COMPOSE_FILE}"

docker compose -f "${COMPOSE_FILE}" ps db | grep -q "healthy" || die "Database container is not healthy"

# ─── Create backup ───────────────────────────────────────────────────────────
log "Running pg_dump..."
docker compose -f "${COMPOSE_FILE}" exec -T db \
    pg_dump \
    -U "${POSTGRES_USER:-madar}" \
    --format=custom \
    --compress=9 \
    "${POSTGRES_DB:-madar_prod}" \
    > "${BACKUP_FILE}" \
    || die "pg_dump failed"

BACKUP_SIZE=$(du -sh "${BACKUP_FILE}" | cut -f1)
log "Backup created: ${BACKUP_FILE} (${BACKUP_SIZE})"

# ─── Verify integrity ────────────────────────────────────────────────────────
log "Verifying backup integrity..."
docker compose -f "${COMPOSE_FILE}" exec -T db \
    pg_restore --list "${BACKUP_FILE}" > /dev/null 2>&1 \
    || die "Backup integrity check failed — file may be corrupted"
log "Integrity verified"

# ─── Upload to S3 ────────────────────────────────────────────────────────────
if [[ -n "${S3_BUCKET}" ]]; then
    log "Uploading to S3: ${S3_BUCKET}/daily/${TIMESTAMP}/"
    aws s3 cp "${BACKUP_FILE}" "${S3_BUCKET}/daily/${TIMESTAMP}/$(basename "${BACKUP_FILE}")" \
        --storage-class STANDARD_IA \
        --sse AES256 \
        || die "Failed to upload to S3"
    log "S3 upload complete"

    # Create a 'latest' symlink in S3
    aws s3 cp "${BACKUP_FILE}" "${S3_BUCKET}/latest/madar_latest.dump" \
        --storage-class STANDARD_IA \
        --sse AES256 2>/dev/null || true
else
    log "WARNING: S3_BACKUP_BUCKET not set — backup is local only"
fi

# ─── Cleanup old local backups ────────────────────────────────────────────────
log "Cleaning up local backups older than ${RETENTION_DAYS_LOCAL} days..."
find "${BACKUP_DIR}" -name "madar_*.sql.gz" -mtime +"${RETENTION_DAYS_LOCAL}" -delete 2>/dev/null || true
find "${BACKUP_DIR}" -name "madar_*.dump" -mtime +"${RETENTION_DAYS_LOCAL}" -delete 2>/dev/null || true
log "Cleanup complete"

# ─── Report success to Prometheus ────────────────────────────────────────────
BACKUP_SIZE_BYTES=$(stat -c%s "${BACKUP_FILE}" 2>/dev/null || stat -f%z "${BACKUP_FILE}" 2>/dev/null || echo 0)
if [[ -n "${PUSHGATEWAY_URL}" ]]; then
    curl -s -X POST "${PUSHGATEWAY_URL}/metrics/job/madar_backup" \
        --data-binary "# HELP madar_backup_success Whether the last backup succeeded (1=success, 0=failure)
# TYPE madar_backup_success gauge
madar_backup_success 1
# HELP madar_backup_timestamp_seconds Unix timestamp of last successful backup
# TYPE madar_backup_timestamp_seconds gauge
madar_backup_timestamp_seconds $(date +%s)
# HELP madar_backup_size_bytes Size of last backup in bytes
# TYPE madar_backup_size_bytes gauge
madar_backup_size_bytes ${BACKUP_SIZE_BYTES}" 2>/dev/null || true
fi

log "✅ Backup completed successfully: ${BACKUP_FILE} (${BACKUP_SIZE})"
