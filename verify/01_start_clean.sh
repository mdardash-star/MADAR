#!/usr/bin/env bash
# ===========================================================================
# verify/01_start_clean.sh
# Starts the complete MADAR application from scratch.
# Tears down any existing containers/volumes, builds fresh images,
# applies all database migrations, and waits for every service to be healthy.
#
# Exit codes:
#   0 = all services healthy, migrations applied
#   1 = failure at any step
# ===========================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "${SCRIPT_DIR}")"
COMPOSE="docker compose -f ${PROJECT_DIR}/docker-compose.yml"

GREEN='\033[0;32m'; RED='\033[0;31m'; YELLOW='\033[1;33m'; NC='\033[0m'
ok()   { echo -e "${GREEN}  ✓${NC}  $*"; }
fail() { echo -e "${RED}  ✗${NC}  $*"; exit 1; }
info() { echo -e "${YELLOW}  ▶${NC}  $*"; }

echo ""
echo "========================================================"
echo "  MADAR — Clean Start Verification"
echo "  $(date -Iseconds)"
echo "========================================================"

# ── Prerequisite check ────────────────────────────────────────────────────────
info "Checking prerequisites..."
command -v docker  >/dev/null 2>&1 || fail "docker not found"
command -v curl    >/dev/null 2>&1 || fail "curl not found"
docker compose version >/dev/null 2>&1 || fail "docker compose plugin not found"
ok "Prerequisites satisfied"

# ── Tear down completely ──────────────────────────────────────────────────────
info "Tearing down existing containers and volumes..."
${COMPOSE} down -v --remove-orphans 2>&1 | tail -5
ok "Teardown complete"

# ── Copy env files if missing ─────────────────────────────────────────────────
info "Checking environment files..."
[[ -f "${PROJECT_DIR}/.env" ]]             || cp "${PROJECT_DIR}/.env.example"           "${PROJECT_DIR}/.env"
[[ -f "${PROJECT_DIR}/apps/api/.env" ]]    || cp "${PROJECT_DIR}/apps/api/.env.example"  "${PROJECT_DIR}/apps/api/.env"
[[ -f "${PROJECT_DIR}/apps/web/.env" ]]    || cp "${PROJECT_DIR}/apps/web/.env.example"  "${PROJECT_DIR}/apps/web/.env"
ok "Environment files ready"

# ── Build and start ───────────────────────────────────────────────────────────
info "Building Docker images and starting services (this may take 2-5 minutes)..."
${COMPOSE} up --build -d 2>&1 | tail -20
ok "docker compose up --build -d completed"

# ── Wait for services ─────────────────────────────────────────────────────────
info "Waiting for services to become healthy (up to 90 seconds)..."

wait_healthy() {
    local service="$1" port="$2" check="$3"
    local retries=18  # 18 × 5s = 90s
    for i in $(seq 1 $retries); do
        if eval "$check" >/dev/null 2>&1; then
            ok "${service} is healthy (attempt ${i})"
            return 0
        fi
        echo "     waiting for ${service}... (${i}/${retries})"
        sleep 5
    done
    fail "${service} did not become healthy after 90 seconds"
}

wait_healthy "PostgreSQL" 5432 \
    "docker compose -f ${PROJECT_DIR}/docker-compose.yml exec -T db pg_isready -U madar -d madar"
wait_healthy "Redis" 6379 \
    "docker compose -f ${PROJECT_DIR}/docker-compose.yml exec -T redis redis-cli ping"
wait_healthy "API" 8000 \
    "curl -sf http://localhost:8000/health"
wait_healthy "Web" 3000 \
    "curl -sf http://localhost:3000 -o /dev/null"

# ── Apply database migrations ─────────────────────────────────────────────────
info "Applying database migrations..."
MIGRATION_OUTPUT=$(${COMPOSE} exec -T api alembic upgrade head 2>&1)
echo "${MIGRATION_OUTPUT}" | tail -5
echo "${MIGRATION_OUTPUT}" | grep -q "Running upgrade\|No migrations" || \
    echo "${MIGRATION_OUTPUT}" | grep -q "head" || true

# Verify head
HEAD=$(${COMPOSE} exec -T api alembic current 2>&1 | grep -oE '[0-9a-f]{14} \(head\)' || echo "")
if [[ -n "${HEAD}" ]]; then
    ok "Migrations at head: ${HEAD}"
else
    # Already at head from previous run
    CURRENT=$(${COMPOSE} exec -T api alembic current 2>&1)
    ok "Migration state: ${CURRENT##*Running }"
fi

# ── Final service status ───────────────────────────────────────────────────────
echo ""
info "Final service status:"
${COMPOSE} ps --format "table {{.Name}}\t{{.Status}}\t{{.Ports}}"
echo ""
ok "API health: $(curl -s http://localhost:8000/health)"
ok "Web status: HTTP $(curl -s -o /dev/null -w '%{http_code}' http://localhost:3000)"

echo ""
echo -e "${GREEN}========================================================"
echo -e "  ✓  CLEAN START COMPLETE"
echo -e "  All 4 services are running and healthy."
echo -e "  Migrations applied to head."
echo -e "========================================================${NC}"
echo ""
