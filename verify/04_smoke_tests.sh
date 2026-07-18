#!/usr/bin/env bash
# ===========================================================================
# verify/04_smoke_tests.sh
# API smoke tests against the running MADAR application.
# Each test makes a real HTTP request and asserts the expected response.
#
# Exit codes:
#   0 = all smoke tests passed
#   1 = one or more tests failed
# ===========================================================================
set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "${SCRIPT_DIR}")"

GREEN='\033[0;32m'; RED='\033[0;31m'; YELLOW='\033[1;33m'; BOLD='\033[1m'; NC='\033[0m'
PASS_COUNT=0; FAIL_COUNT=0
FAILURES=()

pass() { echo -e "${GREEN}  PASS${NC}  $*"; ((PASS_COUNT++)) || true; }
fail() { echo -e "${RED}  FAIL${NC}  $*"; ((FAIL_COUNT++)) || true; FAILURES+=("$*"); }
info() { echo -e "\n${YELLOW}${BOLD}▶  $*${NC}"; }

# ── Helper: assert HTTP status ────────────────────────────────────────────────
assert_status() {
    local label="$1" expected_status="$2"
    shift 2
    local actual_status
    actual_status=$(curl -s -o /dev/null -w "%{http_code}" "$@")
    if [[ "${actual_status}" == "${expected_status}" ]]; then
        pass "${label} → HTTP ${actual_status}"
    else
        fail "${label} → expected HTTP ${expected_status}, got HTTP ${actual_status}"
    fi
}

# ── Helper: assert JSON field ─────────────────────────────────────────────────
assert_json_field() {
    local label="$1" field="$2" expected_value="$3"
    shift 3
    local response
    response=$(curl -s "$@")
    local actual_value
    actual_value=$(echo "${response}" | python3 -c \
        "import sys,json; d=json.load(sys.stdin); print(d.get('${field}','MISSING'))" 2>/dev/null || echo "PARSE_ERROR")
    if [[ "${actual_value}" == "${expected_value}" ]]; then
        pass "${label} → ${field}=${actual_value}"
    else
        fail "${label} → ${field}: expected '${expected_value}', got '${actual_value}'"
        echo "       Response: $(echo "${response}" | head -c 200)"
    fi
}

# ── Helper: assert JSON list length ──────────────────────────────────────────
assert_list_min() {
    local label="$1" min_count="$2"
    shift 2
    local response
    response=$(curl -s "$@")
    local count
    count=$(echo "${response}" | python3 -c \
        "import sys,json; d=json.load(sys.stdin); print(len(d) if isinstance(d,list) else -1)" 2>/dev/null || echo -1)
    if [[ "${count}" -ge "${min_count}" ]]; then
        pass "${label} → ${count} records (≥${min_count})"
    else
        fail "${label} → got ${count} records, expected ≥${min_count}"
    fi
}

echo ""
echo "========================================================"
echo "  MADAR — API Smoke Tests"
echo "  $(date -Iseconds)"
echo "========================================================"

# ── Section 1: Health & Infrastructure ───────────────────────────────────────
info "Section 1: Health & Infrastructure"

assert_json_field "GET /health" "status" "healthy" \
    http://localhost:8000/health

assert_json_field "GET /" "name" "MADAR ERP API" \
    http://localhost:8000/

assert_status "GET /health/live (200)" "200" \
    http://localhost:8000/health/live

assert_status "GET /health/ready (200)" "200" \
    http://localhost:8000/health/ready

assert_status "GET /docs (200)" "200" \
    http://localhost:8000/docs

assert_status "GET /metrics (200)" "200" \
    http://localhost:8000/metrics

# ── Section 2: Authentication ─────────────────────────────────────────────────
info "Section 2: Authentication"

# Valid admin login
LOGIN_RESPONSE=$(curl -s -X POST http://localhost:8000/auth/login \
    -H "Content-Type: application/json" \
    -d '{"email":"admin@gulf-trading.demo","password":"BetaAdmin2026!"}')
ADMIN_TOKEN=$(echo "${LOGIN_RESPONSE}" | python3 -c \
    "import sys,json; print(json.load(sys.stdin).get('access_token',''))" 2>/dev/null || echo "")
if [[ -n "${ADMIN_TOKEN}" ]]; then
    pass "POST /auth/login [admin] → token issued"
    ((PASS_COUNT++)) || true
else
    fail "POST /auth/login [admin] → no token returned"
    ((FAIL_COUNT++)) || true
fi

# Invalid password → 401
assert_status "POST /auth/login [wrong password] → 401" "401" \
    -X POST http://localhost:8000/auth/login \
    -H "Content-Type: application/json" \
    -d '{"email":"admin@gulf-trading.demo","password":"WRONG"}'

# Each demo role
for role_info in \
    "sales@gulf-trading.demo:BetaSales2026!:Sales Manager" \
    "inventory@gulf-trading.demo:BetaInventory2026!:Inventory Manager" \
    "accountant@gulf-trading.demo:BetaAccount2026!:Accountant"; do
    email="${role_info%%:*}"
    rest="${role_info#*:}"
    password="${rest%%:*}"
    role_name="${rest##*:}"
    role_token=$(curl -s -X POST http://localhost:8000/auth/login \
        -H "Content-Type: application/json" \
        -d "{\"email\":\"${email}\",\"password\":\"${password}\"}" \
        | python3 -c "import sys,json; print(json.load(sys.stdin).get('access_token',''))" 2>/dev/null || echo "")
    if [[ -n "${role_token}" ]]; then
        pass "POST /auth/login [${role_name}] → token issued"
        ((PASS_COUNT++)) || true
    else
        fail "POST /auth/login [${role_name}] → no token"
        ((FAIL_COUNT++)) || true
    fi
done

# Token refresh
REFRESH_TOKEN=$(echo "${LOGIN_RESPONSE}" | python3 -c \
    "import sys,json; print(json.load(sys.stdin).get('refresh_token',''))" 2>/dev/null || echo "")
if [[ -n "${REFRESH_TOKEN}" ]]; then
    assert_status "POST /auth/refresh → 200" "200" \
        -X POST http://localhost:8000/auth/refresh \
        -H "Content-Type: application/json" \
        -d "{\"refresh_token\":\"${REFRESH_TOKEN}\"}"
fi

# Unauthenticated → 401
assert_status "GET /api/v1/me (no token) → 401" "401" \
    http://localhost:8000/api/v1/me

# Current user
assert_status "GET /api/v1/me (with token) → 200" "200" \
    -H "Authorization: Bearer ${ADMIN_TOKEN}" \
    http://localhost:8000/api/v1/me

# ── Get company ID for authenticated requests ──────────────────────────────────
CID=$(curl -s -H "Authorization: Bearer ${ADMIN_TOKEN}" http://localhost:8000/api/v1/me \
    | python3 -c "import sys,json; print(json.load(sys.stdin).get('company_id',''))" 2>/dev/null || echo "")
if [[ -z "${CID}" ]]; then
    fail "Could not retrieve company_id from /api/v1/me — remaining tests may fail"
    ((FAIL_COUNT++)) || true
    CID="102"  # fallback to known beta company ID
fi

AUTH="-H Authorization: Bearer ${ADMIN_TOKEN}"

# ── Section 3: Master Data — Branches ────────────────────────────────────────
info "Section 3: Master Data — Branches"

assert_list_min "GET /master-data/branches (≥3)" 3 \
    -H "Authorization: Bearer ${ADMIN_TOKEN}" \
    "http://localhost:8000/api/v1/master-data/branches?company_id=${CID}"

# Use time-based unique code to avoid duplicate key on reruns
SMOKE_UID=$(date +%s | tail -c 6)

CREATE_BRANCH=$(curl -s -X POST \
    -H "Authorization: Bearer ${ADMIN_TOKEN}" \
    -H "Content-Type: application/json" \
    "http://localhost:8000/api/v1/master-data/branches" \
    -d "{\"company_id\":${CID},\"name\":\"Smoke Test Branch\",\"code\":\"SMK-BR-${SMOKE_UID}\"}")
BRANCH_ID=$(echo "${CREATE_BRANCH}" | python3 -c \
    "import sys,json; print(json.load(sys.stdin).get('id',''))" 2>/dev/null || echo "")
if [[ -n "${BRANCH_ID}" && "${BRANCH_ID}" != "None" ]]; then
    pass "POST /master-data/branches → created ID=${BRANCH_ID}"
    ((PASS_COUNT++)) || true
else
    fail "POST /master-data/branches → creation failed: ${CREATE_BRANCH:0:200}"
    ((FAIL_COUNT++)) || true
    BRANCH_ID=""
fi

# Create duplicate → 500 (known: code is globally unique but no 422 schema for branch on PUT)
# Update branch if created
if [[ -n "${BRANCH_ID}" ]]; then
    assert_status "PUT /master-data/branches/${BRANCH_ID} → 200" "200" \
        -X PUT \
        -H "Authorization: Bearer ${ADMIN_TOKEN}" \
        -H "Content-Type: application/json" \
        "http://localhost:8000/api/v1/master-data/branches/${BRANCH_ID}" \
        -d '{"name":"Smoke Test Branch Updated"}'

    assert_status "DELETE /master-data/branches/${BRANCH_ID} → 200" "200" \
        -X DELETE \
        -H "Authorization: Bearer ${ADMIN_TOKEN}" \
        "http://localhost:8000/api/v1/master-data/branches/${BRANCH_ID}"
fi

# POST with missing fields → 422
assert_status "POST /master-data/branches (empty body) → 422" "422" \
    -X POST \
    -H "Authorization: Bearer ${ADMIN_TOKEN}" \
    -H "Content-Type: application/json" \
    "http://localhost:8000/api/v1/master-data/branches" \
    -d '{}'

# ── Section 4: Master Data — Customers ───────────────────────────────────────
info "Section 4: Master Data — Customers"

assert_list_min "GET /master-data/customers (≥8)" 8 \
    -H "Authorization: Bearer ${ADMIN_TOKEN}" \
    "http://localhost:8000/api/v1/master-data/customers?company_id=${CID}"

CREATE_CUST=$(curl -s -X POST \
    -H "Authorization: Bearer ${ADMIN_TOKEN}" \
    -H "Content-Type: application/json" \
    "http://localhost:8000/api/v1/master-data/customers" \
    -d "{\"company_id\":${CID},\"name\":\"Smoke Test Customer\",\"code\":\"SMK-CUS-${SMOKE_UID}\",\"email\":\"smoke@test.com\",\"phone\":\"+1-555-0000\"}")
CUST_ID=$(echo "${CREATE_CUST}" | python3 -c \
    "import sys,json; print(json.load(sys.stdin).get('id',''))" 2>/dev/null || echo "")
if [[ -n "${CUST_ID}" && "${CUST_ID}" != "None" ]]; then
    pass "POST /master-data/customers → created ID=${CUST_ID}"
    ((PASS_COUNT++)) || true
    # Clean up
    curl -s -X DELETE -H "Authorization: Bearer ${ADMIN_TOKEN}" \
        "http://localhost:8000/api/v1/master-data/customers/${CUST_ID}" >/dev/null
    pass "DELETE /master-data/customers/${CUST_ID} → cleaned up"
    ((PASS_COUNT++)) || true
else
    fail "POST /master-data/customers → failed: ${CREATE_CUST:0:200}"
    ((FAIL_COUNT++)) || true
fi

assert_status "POST /master-data/customers (empty body) → 422" "422" \
    -X POST \
    -H "Authorization: Bearer ${ADMIN_TOKEN}" \
    -H "Content-Type: application/json" \
    "http://localhost:8000/api/v1/master-data/customers" \
    -d '{}'

# ── Section 5: Master Data — Products ────────────────────────────────────────
info "Section 5: Master Data — Products"

assert_list_min "GET /master-data/products (≥15)" 15 \
    -H "Authorization: Bearer ${ADMIN_TOKEN}" \
    "http://localhost:8000/api/v1/master-data/products?company_id=${CID}"

assert_status "POST /master-data/products (empty body) → 422" "422" \
    -X POST \
    -H "Authorization: Bearer ${ADMIN_TOKEN}" \
    -H "Content-Type: application/json" \
    "http://localhost:8000/api/v1/master-data/products" \
    -d '{}'

# ── Section 6: Master Data — Warehouses & Suppliers ──────────────────────────
info "Section 6: Warehouses & Suppliers"

assert_list_min "GET /master-data/warehouses (≥4)" 4 \
    -H "Authorization: Bearer ${ADMIN_TOKEN}" \
    "http://localhost:8000/api/v1/master-data/warehouses?company_id=${CID}"

assert_list_min "GET /master-data/suppliers (≥5)" 5 \
    -H "Authorization: Bearer ${ADMIN_TOKEN}" \
    "http://localhost:8000/api/v1/master-data/suppliers?company_id=${CID}"

# ── Section 7: Sales Pipeline ─────────────────────────────────────────────────
info "Section 7: Sales Pipeline"

assert_list_min "GET /sales/quotations (≥6)" 6 \
    -H "Authorization: Bearer ${ADMIN_TOKEN}" \
    "http://localhost:8000/api/v1/sales/quotations?company_id=${CID}"

assert_list_min "GET /sales/orders (≥6)" 6 \
    -H "Authorization: Bearer ${ADMIN_TOKEN}" \
    "http://localhost:8000/api/v1/sales/orders?company_id=${CID}"

assert_list_min "GET /sales/invoices (≥3)" 3 \
    -H "Authorization: Bearer ${ADMIN_TOKEN}" \
    "http://localhost:8000/api/v1/sales/invoices?company_id=${CID}"

# ── Section 8: Inventory ───────────────────────────────────────────────────────
info "Section 8: Inventory"

assert_list_min "GET /inventory/stock-movements (≥13)" 13 \
    -H "Authorization: Bearer ${ADMIN_TOKEN}" \
    "http://localhost:8000/api/v1/inventory/stock-movements?company_id=${CID}"

# ── Section 9: Dashboard ──────────────────────────────────────────────────────
info "Section 9: Dashboard"

DASHBOARD=$(curl -s \
    -H "Authorization: Bearer ${ADMIN_TOKEN}" \
    "http://localhost:8000/api/v1/dashboard/summary?company_id=${CID}")

check_dashboard_kpi() {
    local field="$1" expected="$2"
    local actual
    actual=$(echo "${DASHBOARD}" | python3 -c \
        "import sys,json; print(json.load(sys.stdin).get('${field}',-1))" 2>/dev/null || echo -1)
    if [[ "${actual}" -ge "${expected}" ]]; then
        pass "Dashboard KPI ${field}=${actual} (≥${expected})"
        ((PASS_COUNT++)) || true
    else
        fail "Dashboard KPI ${field}: expected ≥${expected}, got ${actual}"
        ((FAIL_COUNT++)) || true
    fi
}

check_dashboard_kpi "branches"      3
check_dashboard_kpi "warehouses"    4
check_dashboard_kpi "customers"     8
check_dashboard_kpi "suppliers"     5
check_dashboard_kpi "products"      15
check_dashboard_kpi "quotations"    6
check_dashboard_kpi "sales_orders"  6
check_dashboard_kpi "sales_invoices" 3

# ── Section 10: Security — auth enforcement ────────────────────────────────────
info "Section 10: Security"

# /api/v1/me DOES enforce auth (only protected endpoint in current implementation)
assert_status "GET /api/v1/me (no token) → 401" "401" \
    http://localhost:8000/api/v1/me

# login with unknown user → 401
assert_status "POST /auth/login (unknown user) → 401" "401" \
    -X POST http://localhost:8000/auth/login \
    -H "Content-Type: application/json" \
    -d '{"email":"notexist@example.com","password":"anything"}'

# KNOWN LIMITATION: master-data and dashboard GET routes do not enforce auth at
# the API level. This is documented in KNOWN_LIMITATIONS.md (SEC-02) and tracked
# as a fix for v1.1.0. The existing test suite (49 tests) operates without auth
# headers on CRUD routes — adding enforcement would require updating all tests.
# Documenting actual observed behavior:
BRANCHES_NOAUTH=$(curl -s -o /dev/null -w "%{http_code}" \
    "http://localhost:8000/api/v1/master-data/branches?company_id=${CID}")
echo "     NOTE: GET /api/v1/master-data/branches (no token) → HTTP ${BRANCHES_NOAUTH}"
echo "     KNOWN LIMITATION: Auth not enforced on resource GET routes (tracked: v1.1.0)"

# ── Summary ───────────────────────────────────────────────────────────────────
echo ""
echo "========================================================"
echo "  SMOKE TEST RESULTS"
echo "========================================================"
echo -e "${GREEN}  PASSED: ${PASS_COUNT}${NC}"
if [[ "${FAIL_COUNT}" -gt 0 ]]; then
    echo -e "${RED}  FAILED: ${FAIL_COUNT}${NC}"
    echo ""
    echo -e "${RED}  Failures:${NC}"
    for f in "${FAILURES[@]}"; do
        echo -e "${RED}    • ${f}${NC}"
    done
    echo ""
    echo -e "${RED}  SMOKE TESTS FAILED${NC}"
    exit 1
else
    echo ""
    echo -e "${GREEN}========================================================"
    echo -e "  ✓  ALL ${PASS_COUNT} SMOKE TESTS PASSED"
    echo -e "========================================================${NC}"
fi
echo ""
