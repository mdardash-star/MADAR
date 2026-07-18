#!/usr/bin/env bash
# ============================================================
# MADAR Database Restore Script
# ============================================================
# Usage:
#   ./scripts/restore.sh <backup-file>
#   ./scripts/restore.sh s3://madar-backups/latest/madar_latest.dump
#   ./scripts/restore.sh  (lists available backups and prompts)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "${SCRIPT_DIR}")"
COMPOSE_FILE="${COMPOSE_FILE:-${PROJECT_DIR}/docker-compose.prod.yml}"
BACKUP_DIR="${PROJECT_DIR}/backups"
LOG_FILE="/var/log/madar/restore.log"
S3_BUCKET="${S3_BACKUP_BUCKET:-}"

mkdir -p "$(dirname "${LOG_FILE}" 2>/dev/null)" 2>/dev/null || true

log() {
    local msg="[$(date -Iseconds)] $*"
    echo "${msg}"
    echo "${msg}" >> "${LOG_FILE}" 2>/dev/null || true
}

die() { log "ERROR: $*"; exit 1; }

# ─── Show available backups if no argument ───────────────────────────────────
BACKUP_FILE="${1:-}"

if [[ -z "${BACKUP_FILE}" ]]; then
    echo ""
    echo "Available local backups:"
    ls -lt "${BACKUP_DIR}"/*.dump 2>/dev/null | head -10 || echo "  (none found)"
    echo ""
    if [[ -n "${S3_BUCKET}" ]]; then
        echo "S3 backups (most recent 10):"
        aws s3 ls "${S3_BUCKET}/daily/" | sort -r | head -10 || true
    fi
    echo ""
    echo "Usage: $0 <backup-file-or-s3-path>"
    exit 0
fi

# ─── Safety confirmation ─────────────────────────────────────────────────────
log "RESTORE OPERATION REQUESTED"
log "  Source: ${BACKUP_FILE}"
log "  Target: ${POSTGRES_DB:-madar_prod}"
log ""
echo ""
echo "⚠️  WARNING: This will OVERWRITE the production database!"
echo "   Source: ${BACKUP_FILE}"
echo "   Target: ${POSTGRES_DB:-madar_prod}"
echo ""
read -rp "Type 'CONFIRM RESTORE' to proceed: " CONFIRM
[[ "${CONFIRM}" == "CONFIRM RESTORE" ]] || { log "Restore cancelled by user"; exit 0; }

# ─── Download from S3 if needed ──────────────────────────────────────────────
if [[ "${BACKUP_FILE}" == s3://* ]]; then
    LOCAL_FILE="${BACKUP_DIR}/restore_$(date +%s).dump"
    log "Downloading from S3: ${BACKUP_FILE}"
    aws s3 cp "${BACKUP_FILE}" "${LOCAL_FILE}" || die "Failed to download from S3"
    BACKUP_FILE="${LOCAL_FILE}"
    CLEANUP_TEMP=true
fi

[[ -f "${BACKUP_FILE}" ]] || die "Backup file not found: ${BACKUP_FILE}"

# ─── Verify backup before proceeding ────────────────────────────────────────
log "Verifying backup integrity..."
docker compose -f "${COMPOSE_FILE}" exec -T db \
    pg_restore --list "${BACKUP_FILE}" > /dev/null 2>&1 \
    || die "Backup integrity check failed"
log "Backup verified"

# ─── Safety snapshot of current state ───────────────────────────────────────
SAFETY_BACKUP="${BACKUP_DIR}/pre-restore_$(date +%Y%m%d_%H%M%S).dump"
log "Creating safety snapshot: ${SAFETY_BACKUP}"
docker compose -f "${COMPOSE_FILE}" exec -T db \
    pg_dump -U "${POSTGRES_USER:-madar}" --format=custom --compress=9 \
    "${POSTGRES_DB:-madar_prod}" > "${SAFETY_BACKUP}" \
    || log "WARNING: Could not create safety snapshot — proceeding anyway"

# ─── Stop application ────────────────────────────────────────────────────────
log "Stopping application services..."
docker compose -f "${COMPOSE_FILE}" stop api web 2>/dev/null || true

# ─── Terminate active DB connections ─────────────────────────────────────────
log "Terminating active database connections..."
docker compose -f "${COMPOSE_FILE}" exec -T db psql \
    -U "${POSTGRES_USER:-madar}" \
    -c "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname='${POSTGRES_DB:-madar_prod}' AND pid <> pg_backend_pid();" 2>/dev/null || true

# ─── Drop and recreate database ──────────────────────────────────────────────
log "Recreating database..."
docker compose -f "${COMPOSE_FILE}" exec -T db psql \
    -U "${POSTGRES_USER:-madar}" \
    -c "DROP DATABASE IF EXISTS \"${POSTGRES_DB:-madar_prod}\"; CREATE DATABASE \"${POSTGRES_DB:-madar_prod}\";" \
    || die "Failed to recreate database"

# ─── Restore backup ──────────────────────────────────────────────────────────
log "Restoring backup (this may take a few minutes)..."
docker compose -f "${COMPOSE_FILE}" exec -T db \
    pg_restore -U "${POSTGRES_USER:-madar}" \
    --dbname="${POSTGRES_DB:-madar_prod}" \
    --no-owner \
    --no-acl \
    --jobs=2 \
    "${BACKUP_FILE}" \
    || log "WARNING: Some restore errors occurred (may be non-critical)"

log "Restore completed"

# ─── Restart application ─────────────────────────────────────────────────────
log "Restarting application services..."
docker compose -f "${COMPOSE_FILE}" start api web

# ─── Health check ─────────────────────────────────────────────────────────────
log "Waiting for API to become healthy..."
RETRIES=10
for i in $(seq 1 ${RETRIES}); do
    if curl -sf http://localhost:8000/health > /dev/null 2>&1; then
        log "✅ API is healthy"
        break
    fi
    log "  Attempt ${i}/${RETRIES} — waiting..."
    sleep 10
    if [[ ${i} -eq ${RETRIES} ]]; then
        log ""
        log "❌ API health check failed after restore!"
        log "   To rollback, restore the safety snapshot:"
        log "   $0 ${SAFETY_BACKUP}"
        exit 1
    fi
done

# ─── Cleanup temp download ────────────────────────────────────────────────────
if [[ "${CLEANUP_TEMP:-false}" == "true" ]]; then
    rm -f "${BACKUP_FILE}" 2>/dev/null || true
fi

log ""
log "✅ Database restore completed successfully"
log "   Safety snapshot: ${SAFETY_BACKUP}"
log "   (Keep for 48 hours then delete manually)"
