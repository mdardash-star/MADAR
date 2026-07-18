#!/usr/bin/env bash
# ===========================================================================
# verify/03_seed_demo.sh
# Seeds the beta demo database (Gulf Electronics & Trading Ltd).
# Idempotent — safe to run multiple times.
#
# Exit codes:
#   0 = seeding completed successfully
#   1 = failure
# ===========================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "${SCRIPT_DIR}")"
COMPOSE="docker compose -f ${PROJECT_DIR}/docker-compose.yml"

GREEN='\033[0;32m'; RED='\033[0;31m'; YELLOW='\033[1;33d'; NC='\033[0m'
GREEN='\033[0;32m'; RED='\033[0;31m'; YELLOW='\033[1;33m'; NC='\033[0m'
ok()   { echo -e "${GREEN}  ✓${NC}  $*"; }
fail() { echo -e "${RED}  ✗${NC}  $*"; exit 1; }
info() { echo -e "${YELLOW}  ▶${NC}  $*"; }

echo ""
echo "========================================================"
echo "  MADAR — Demo Data Seeding"
echo "  $(date -Iseconds)"
echo "========================================================"

# ── Prerequisite ──────────────────────────────────────────────────────────────
info "Checking API health..."
curl -sf http://localhost:8000/health >/dev/null 2>&1 || \
    fail "API is not healthy — run 01_start_clean.sh first"
ok "API is healthy"

# ── Copy script into container ────────────────────────────────────────────────
info "Copying beta_seed.py into API container..."
docker cp "${PROJECT_DIR}/apps/api/scripts/beta_seed.py" madar-api-1:/app/scripts/beta_seed.py \
    2>/dev/null || fail "Failed to copy seed script — is madar-api-1 running?"
ok "Script copied"

# ── Run the seed ──────────────────────────────────────────────────────────────
info "Running beta_seed.py..."
SEED_OUTPUT=$(${COMPOSE} exec -T api sh -c "cd /app && PYTHONPATH=/app python scripts/beta_seed.py" 2>&1)

echo "${SEED_OUTPUT}"

# ── Validate output ───────────────────────────────────────────────────────────
echo ""
echo "========================================================"
echo "  SEED VALIDATION"
echo "========================================================"

check_seeded() {
    local label="$1" pattern="$2"
    if echo "${SEED_OUTPUT}" | grep -q "${pattern}"; then
        ok "${label}"
    else
        echo -e "${RED}  ✗  ${label} — NOT FOUND in seed output${NC}"
        return 1
    fi
}

check_seeded "Company created/verified"      "Gulf Electronics"
check_seeded "Branches seeded"               "Branches"
check_seeded "Warehouses seeded"             "Warehouses"
check_seeded "Roles created"                 "Role \[admin\]"
check_seeded "Sales Manager role"            "Role \[sales-manager\]"
check_seeded "Inventory Manager role"        "Role \[inventory-manager\]"
check_seeded "Accountant role"               "Role \[accountant\]"
check_seeded "Admin user"                    "admin@gulf-trading.demo"
check_seeded "Sales Manager user"            "sales@gulf-trading.demo"
check_seeded "Inventory Manager user"        "inventory@gulf-trading.demo"
check_seeded "Accountant user"               "accountant@gulf-trading.demo"
check_seeded "Customers seeded"              "customers seeded"
check_seeded "Suppliers seeded"              "suppliers seeded"
check_seeded "Products seeded"               "products seeded"
check_seeded "Quotations seeded"             "quotations seeded"
check_seeded "Orders seeded"                 "orders seeded"
check_seeded "Invoices seeded"               "invoices seeded"

# ── Verify via API ─────────────────────────────────────────────────────────────
info "Verifying seeded data via API..."
TOKEN=$(curl -s -X POST http://localhost:8000/auth/login \
    -H "Content-Type: application/json" \
    -d '{"email":"admin@gulf-trading.demo","password":"BetaAdmin2026!"}' \
    | python3 -c "import sys,json; print(json.load(sys.stdin).get('access_token',''))" 2>/dev/null)

[[ -n "${TOKEN}" ]] || fail "Could not authenticate as admin@gulf-trading.demo"
ok "Admin login: OK"

CID=$(curl -s -H "Authorization: Bearer ${TOKEN}" http://localhost:8000/api/v1/me \
    | python3 -c "import sys,json; print(json.load(sys.stdin).get('company_id',''))" 2>/dev/null)
[[ -n "${CID}" ]] || fail "Could not retrieve company_id"
ok "Company ID: ${CID}"

verify_count() {
    local label="$1" endpoint="$2" min_count="$3"
    local count
    count=$(curl -s -H "Authorization: Bearer ${TOKEN}" \
        "http://localhost:8000/api/v1/${endpoint}?company_id=${CID}" \
        | python3 -c "import sys,json; d=json.load(sys.stdin); print(len(d) if isinstance(d,list) else -1)" 2>/dev/null || echo -1)
    if [[ "${count}" -ge "${min_count}" ]]; then
        ok "${label}: ${count} records (expected ≥${min_count})"
    else
        echo -e "${RED}  ✗  ${label}: got ${count}, expected ≥${min_count}${NC}"
        return 1
    fi
}

verify_count "Branches"          "master-data/branches"     3
verify_count "Warehouses"        "master-data/warehouses"   4
verify_count "Customers"         "master-data/customers"    8
verify_count "Suppliers"         "master-data/suppliers"    5
verify_count "Products"          "master-data/products"     15
verify_count "Quotations"        "sales/quotations"         6
verify_count "Orders"            "sales/orders"             6
verify_count "Invoices"          "sales/invoices"           3
verify_count "Stock Movements"   "inventory/stock-movements" 13

echo ""
echo -e "${GREEN}========================================================"
echo -e "  ✓  DEMO DATA SEEDING COMPLETE"
echo -e "  Company: Gulf Electronics & Trading Ltd"
echo -e "  Credentials:"
echo -e "    admin@gulf-trading.demo    / BetaAdmin2026!"
echo -e "    sales@gulf-trading.demo    / BetaSales2026!"
echo -e "    inventory@gulf-trading.demo/ BetaInventory2026!"
echo -e "    accountant@gulf-trading.demo/ BetaAccount2026!"
echo -e "========================================================${NC}"
echo ""
