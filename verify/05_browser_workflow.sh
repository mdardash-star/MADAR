#!/usr/bin/env bash
# ===========================================================================
# verify/05_browser_workflow.sh
# Verifies the complete end-to-end browser workflow by driving the API
# directly (no browser automation tool available in this environment).
# Tests the exact sequence a user would perform in the browser.
#
# Workflow covered:
#   1. Register a new company
#   2. Login
#   3. Create branch → warehouse → customer → supplier → product
#   4. Create quotation → order → invoice
#   5. Record stock movement
#   6. Verify dashboard KPIs updated
#   7. Verify frontend serves all 12 pages (HTTP 200)
#
# Exit codes:
#   0 = all workflow steps completed
#   1 = failure
# ===========================================================================
set -uo pipefail

GREEN='\033[0;32m'; RED='\033[0;31m'; YELLOW='\033[1;33m'; BOLD='\033[1m'; NC='\033[0m'
STEP=0; PASS_COUNT=0; FAIL_COUNT=0

step() {
    ((STEP++)) || true
    echo -e "\n${YELLOW}${BOLD}Step ${STEP}: $*${NC}"
}
pass() { echo -e "${GREEN}  ✓${NC}  $*"; ((PASS_COUNT++)) || true; }
fail() {
    echo -e "${RED}  ✗${NC}  $*"
    ((FAIL_COUNT++)) || true
    # Print context and abort workflow
    echo -e "${RED}  WORKFLOW ABORTED at step ${STEP}${NC}"
    echo ""
    echo "  RESULT: ${PASS_COUNT} passed, ${FAIL_COUNT} failed"
    exit 1
}
info() { echo "     $*"; }

echo ""
echo "========================================================"
echo "  MADAR — End-to-End Browser Workflow Verification"
echo "  $(date -Iseconds)"
echo "========================================================"

# ── Prereq check ──────────────────────────────────────────────────────────────
step "Pre-flight: API and Frontend are reachable"
API_HEALTH=$(curl -s http://localhost:8000/health 2>/dev/null || echo "")
[[ "${API_HEALTH}" == '{"status":"healthy"}' ]] || \
    fail "API not healthy: ${API_HEALTH} — run 01_start_clean.sh first"
pass "API: $(curl -s http://localhost:8000/health)"

WEB_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:3000 2>/dev/null || echo "0")
[[ "${WEB_STATUS}" == "200" ]] || fail "Frontend not reachable: HTTP ${WEB_STATUS}"
pass "Frontend: HTTP ${WEB_STATUS}"

# ── Step 1: Register a new test company ───────────────────────────────────────
UNIQ=$(date +%s | tail -c 6)
TEST_SLUG="wf-test-${UNIQ}"
TEST_EMAIL="admin@${TEST_SLUG}.demo"
TEST_PASSWORD="Workflow2026!"

step "Register new company (simulates registration page)"
REG=$(curl -s -X POST http://localhost:8000/companies/register \
    -H "Content-Type: application/json" \
    -d "{
        \"company_name\": \"Workflow Test Co ${UNIQ}\",
        \"company_slug\": \"${TEST_SLUG}\",
        \"admin_email\": \"${TEST_EMAIL}\",
        \"admin_password\": \"${TEST_PASSWORD}\",
        \"admin_full_name\": \"WF Test Admin\"
    }")
CID=$(echo "${REG}" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('company',{}).get('id','') or d.get('id',''))" 2>/dev/null || echo "")
[[ -n "${CID}" && "${CID}" != "None" ]] || fail "Registration failed: ${REG:0:300}"
pass "Company registered: ID=${CID}, slug=${TEST_SLUG}"

# ── Step 2: Login ──────────────────────────────────────────────────────────────
step "Login (simulates login page)"
LOGIN=$(curl -s -X POST http://localhost:8000/auth/login \
    -H "Content-Type: application/json" \
    -d "{\"email\":\"${TEST_EMAIL}\",\"password\":\"${TEST_PASSWORD}\"}")
TOKEN=$(echo "${LOGIN}" | python3 -c "import sys,json; print(json.load(sys.stdin).get('access_token',''))" 2>/dev/null || echo "")
[[ -n "${TOKEN}" ]] || fail "Login failed: ${LOGIN:0:300}"
pass "Login successful — JWT token issued"

ME=$(curl -s -H "Authorization: Bearer ${TOKEN}" http://localhost:8000/api/v1/me)
USER_NAME=$(echo "${ME}" | python3 -c "import sys,json; print(json.load(sys.stdin).get('full_name',''))" 2>/dev/null || echo "")
pass "Current user: ${USER_NAME} (company_id=${CID})"

# ── Step 3: View Dashboard ─────────────────────────────────────────────────────
step "View Dashboard (simulates dashboard page load)"
DASH=$(curl -s -H "Authorization: Bearer ${TOKEN}" \
    "http://localhost:8000/api/v1/dashboard/summary?company_id=${CID}")
DASH_BRANCHES=$(echo "${DASH}" | python3 -c "import sys,json; print(json.load(sys.stdin).get('branches',0))" 2>/dev/null || echo -1)
[[ "${DASH_BRANCHES}" -ge 0 ]] || fail "Dashboard KPI call failed: ${DASH:0:200}"
pass "Dashboard loaded — branches=${DASH_BRANCHES} (newly registered company)"

# ── Step 4: Create Branch ──────────────────────────────────────────────────────
step "Create Branch (simulates Branches → Add Branch)"
BR=$(curl -s -X POST \
    -H "Authorization: Bearer ${TOKEN}" \
    -H "Content-Type: application/json" \
    "http://localhost:8000/api/v1/master-data/branches" \
    -d "{\"company_id\":${CID},\"name\":\"Main Office\",\"code\":\"WF-BR-${UNIQ}\",\"country\":\"Saudi Arabia\",\"city\":\"Riyadh\",\"timezone\":\"Asia/Riyadh\"}")
BR_ID=$(echo "${BR}" | python3 -c "import sys,json; print(json.load(sys.stdin).get('id',''))" 2>/dev/null || echo "")
[[ -n "${BR_ID}" && "${BR_ID}" != "None" ]] || fail "Branch creation failed: ${BR:0:300}"
pass "Branch created: ID=${BR_ID}"

# ── Step 5: Create Warehouse ───────────────────────────────────────────────────
step "Create Warehouse (simulates Warehouses → Add Warehouse)"
WH=$(curl -s -X POST \
    -H "Authorization: Bearer ${TOKEN}" \
    -H "Content-Type: application/json" \
    "http://localhost:8000/api/v1/master-data/warehouses" \
    -d "{\"company_id\":${CID},\"branch_id\":${BR_ID},\"name\":\"Main Warehouse\",\"code\":\"WF-WH-${UNIQ}\",\"address\":\"Industrial Zone, Riyadh\"}")
WH_ID=$(echo "${WH}" | python3 -c "import sys,json; print(json.load(sys.stdin).get('id',''))" 2>/dev/null || echo "")
[[ -n "${WH_ID}" && "${WH_ID}" != "None" ]] || fail "Warehouse creation failed: ${WH:0:300}"
pass "Warehouse created: ID=${WH_ID}"

# ── Step 6: Create Customer ────────────────────────────────────────────────────
step "Create Customer (simulates Customers → Add Customer)"
CUST=$(curl -s -X POST \
    -H "Authorization: Bearer ${TOKEN}" \
    -H "Content-Type: application/json" \
    "http://localhost:8000/api/v1/master-data/customers" \
    -d "{\"company_id\":${CID},\"name\":\"WF Test Customer\",\"code\":\"WF-CUS-${UNIQ}\",\"email\":\"customer@wftest.com\",\"phone\":\"+966-11-0000001\"}")
CUST_ID=$(echo "${CUST}" | python3 -c "import sys,json; print(json.load(sys.stdin).get('id',''))" 2>/dev/null || echo "")
[[ -n "${CUST_ID}" && "${CUST_ID}" != "None" ]] || fail "Customer creation failed: ${CUST:0:300}"
pass "Customer created: ID=${CUST_ID}"

# ── Step 7: Create Supplier ────────────────────────────────────────────────────
step "Create Supplier (simulates Suppliers → Add Supplier)"
SUP=$(curl -s -X POST \
    -H "Authorization: Bearer ${TOKEN}" \
    -H "Content-Type: application/json" \
    "http://localhost:8000/api/v1/master-data/suppliers" \
    -d "{\"company_id\":${CID},\"name\":\"WF Test Supplier\",\"code\":\"WF-SUP-${UNIQ}\",\"email\":\"supplier@wftest.com\",\"phone\":\"+971-4-0000001\"}")
SUP_ID=$(echo "${SUP}" | python3 -c "import sys,json; print(json.load(sys.stdin).get('id',''))" 2>/dev/null || echo "")
[[ -n "${SUP_ID}" && "${SUP_ID}" != "None" ]] || fail "Supplier creation failed: ${SUP:0:300}"
pass "Supplier created: ID=${SUP_ID}"

# ── Step 8: Create Product (need category + UoM) ──────────────────────────────
step "Create Product (simulates Products → Add Product)"
# Get first category and UoM for this company (may be from another company but IDs are global)
CAT_ID=$(curl -s \
    -H "Authorization: Bearer ${TOKEN}" \
    "http://localhost:8000/api/v1/master-data/product-categories?company_id=${CID}" \
    | python3 -c "import sys,json; d=json.load(sys.stdin); print(d[0]['id'] if d else '')" 2>/dev/null || echo "")

UOM_ID=$(curl -s \
    -H "Authorization: Bearer ${TOKEN}" \
    "http://localhost:8000/api/v1/master-data/units-of-measure?company_id=${CID}" \
    | python3 -c "import sys,json; d=json.load(sys.stdin); print(d[0]['id'] if d else '')" 2>/dev/null || echo "")

if [[ -z "${CAT_ID}" || -z "${UOM_ID}" ]]; then
    # Create category and UoM for this company
    CAT=$(curl -s -X POST \
        -H "Authorization: Bearer ${TOKEN}" \
        -H "Content-Type: application/json" \
        "http://localhost:8000/api/v1/master-data/product-categories" \
        -d "{\"company_id\":${CID},\"name\":\"WF Category\",\"code\":\"WF-CAT-${UNIQ}\"}")
    CAT_ID=$(echo "${CAT}" | python3 -c "import sys,json; print(json.load(sys.stdin).get('id',''))" 2>/dev/null || echo "")

    UOM=$(curl -s -X POST \
        -H "Authorization: Bearer ${TOKEN}" \
        -H "Content-Type: application/json" \
        "http://localhost:8000/api/v1/master-data/units-of-measure" \
        -d "{\"company_id\":${CID},\"name\":\"WF Piece\",\"code\":\"WF-PC-${UNIQ}\",\"abbreviation\":\"pc\"}")
    UOM_ID=$(echo "${UOM}" | python3 -c "import sys,json; print(json.load(sys.stdin).get('id',''))" 2>/dev/null || echo "")
fi

info "Using category_id=${CAT_ID}, unit_of_measure_id=${UOM_ID}"

PROD=$(curl -s -X POST \
    -H "Authorization: Bearer ${TOKEN}" \
    -H "Content-Type: application/json" \
    "http://localhost:8000/api/v1/master-data/products" \
    -d "{\"company_id\":${CID},\"name\":\"WF Test Product\",\"sku\":\"WF-SKU-${UNIQ}\",\"category_id\":${CAT_ID},\"unit_of_measure_id\":${UOM_ID},\"cost_price\":100.00,\"selling_price\":150.00}")
PROD_ID=$(echo "${PROD}" | python3 -c "import sys,json; print(json.load(sys.stdin).get('id',''))" 2>/dev/null || echo "")
[[ -n "${PROD_ID}" && "${PROD_ID}" != "None" ]] || fail "Product creation failed: ${PROD:0:300}"
pass "Product created: ID=${PROD_ID}"

# ── Step 9: Create Quotation ──────────────────────────────────────────────────
step "Create Quotation (simulates Quotations → Create)"
TODAY=$(date +%Y-%m-%d)
FUTURE=$(date -d "+30 days" +%Y-%m-%d 2>/dev/null || date -v+30d +%Y-%m-%d 2>/dev/null || echo "2026-08-17")
QT=$(curl -s -X POST \
    -H "Authorization: Bearer ${TOKEN}" \
    -H "Content-Type: application/json" \
    "http://localhost:8000/api/v1/sales/quotations" \
    -d "{\"company_id\":${CID},\"customer_id\":${CUST_ID},\"warehouse_id\":${WH_ID},\"code\":\"WF-QT-${UNIQ}\",\"quote_date\":\"${TODAY}\",\"valid_until\":\"${FUTURE}\",\"status\":\"draft\",\"subtotal_amount\":150.00,\"tax_amount\":22.50,\"discount_amount\":0.00,\"total_amount\":172.50}")
QT_ID=$(echo "${QT}" | python3 -c "import sys,json; print(json.load(sys.stdin).get('id',''))" 2>/dev/null || echo "")
[[ -n "${QT_ID}" && "${QT_ID}" != "None" ]] || fail "Quotation creation failed: ${QT:0:300}"
pass "Quotation created: ID=${QT_ID}"

# ── Step 10: Create Sales Order ────────────────────────────────────────────────
step "Create Sales Order (simulates Orders → Create)"
SO=$(curl -s -X POST \
    -H "Authorization: Bearer ${TOKEN}" \
    -H "Content-Type: application/json" \
    "http://localhost:8000/api/v1/sales/orders" \
    -d "{\"company_id\":${CID},\"customer_id\":${CUST_ID},\"warehouse_id\":${WH_ID},\"code\":\"WF-SO-${UNIQ}\",\"order_date\":\"${TODAY}\",\"status\":\"confirmed\",\"subtotal_amount\":150.00,\"tax_amount\":22.50,\"discount_amount\":0.00,\"total_amount\":172.50,\"payment_status\":\"pending\"}")
SO_ID=$(echo "${SO}" | python3 -c "import sys,json; print(json.load(sys.stdin).get('id',''))" 2>/dev/null || echo "")
[[ -n "${SO_ID}" && "${SO_ID}" != "None" ]] || fail "Sales Order creation failed: ${SO:0:300}"
pass "Sales Order created: ID=${SO_ID}"

# ── Step 11: Create Invoice ────────────────────────────────────────────────────
step "Create Invoice (simulates Invoices → Create)"
INV=$(curl -s -X POST \
    -H "Authorization: Bearer ${TOKEN}" \
    -H "Content-Type: application/json" \
    "http://localhost:8000/api/v1/sales/invoices" \
    -d "{\"company_id\":${CID},\"customer_id\":${CUST_ID},\"order_id\":${SO_ID},\"warehouse_id\":${WH_ID},\"code\":\"WF-INV-${UNIQ}\",\"invoice_date\":\"${TODAY}\",\"due_date\":\"${FUTURE}\",\"status\":\"issued\",\"subtotal_amount\":150.00,\"tax_amount\":22.50,\"discount_amount\":0.00,\"total_amount\":172.50,\"payment_status\":\"pending\"}")
INV_ID=$(echo "${INV}" | python3 -c "import sys,json; print(json.load(sys.stdin).get('id',''))" 2>/dev/null || echo "")
[[ -n "${INV_ID}" && "${INV_ID}" != "None" ]] || fail "Invoice creation failed: ${INV:0:300}"
pass "Invoice created: ID=${INV_ID}"

# ── Step 12: Record Stock Movement ────────────────────────────────────────────
step "Record Stock Movement (simulates Inventory → New Movement)"
MOV=$(curl -s -X POST \
    -H "Authorization: Bearer ${TOKEN}" \
    -H "Content-Type: application/json" \
    "http://localhost:8000/api/v1/inventory/stock-movements" \
    -d "{\"company_id\":${CID},\"product_id\":${PROD_ID},\"warehouse_id\":${WH_ID},\"quantity\":50,\"movement_type\":\"purchase\",\"reference_type\":\"supplier\",\"reference_id\":${SUP_ID},\"movement_date\":\"${TODAY}\",\"note\":\"WF smoke test stock receipt\"}")
MOV_ID=$(echo "${MOV}" | python3 -c "import sys,json; print(json.load(sys.stdin).get('id',''))" 2>/dev/null || echo "")
[[ -n "${MOV_ID}" && "${MOV_ID}" != "None" ]] || fail "Stock movement creation failed: ${MOV:0:300}"
pass "Stock Movement created: ID=${MOV_ID}"

# ── Step 13: Verify Dashboard KPIs updated ─────────────────────────────────────
step "Verify Dashboard KPIs reflect all created data"
DASH2=$(curl -s -H "Authorization: Bearer ${TOKEN}" \
    "http://localhost:8000/api/v1/dashboard/summary?company_id=${CID}")

assert_kpi() {
    local field="$1" expected="$2"
    local actual
    actual=$(echo "${DASH2}" | python3 -c "import sys,json; print(json.load(sys.stdin).get('${field}',0))" 2>/dev/null || echo 0)
    if [[ "${actual}" -ge "${expected}" ]]; then
        pass "Dashboard.${field}=${actual} (≥${expected})"
    else
        fail "Dashboard.${field}=${actual} expected ≥${expected}"
    fi
}

assert_kpi "branches"      1
assert_kpi "warehouses"    1
assert_kpi "customers"     1
assert_kpi "suppliers"     1
assert_kpi "products"      1
assert_kpi "quotations"    1
assert_kpi "sales_orders"  1
assert_kpi "sales_invoices" 1

# ── Step 14: Verify Frontend Pages ────────────────────────────────────────────
step "Verify frontend routes serve HTTP 200"
FRONTEND_ROUTES=(
    "/"
    "/login"
    "/register"
    "/dashboard"
    "/branches"
    "/warehouses"
    "/customers"
    "/suppliers"
    "/products"
    "/quotations"
    "/orders"
    "/invoices"
    "/profile"
)
for route in "${FRONTEND_ROUTES[@]}"; do
    status=$(curl -s -o /dev/null -w "%{http_code}" "http://localhost:3000${route}" 2>/dev/null || echo "0")
    if [[ "${status}" == "200" ]]; then
        pass "GET http://localhost:3000${route} → HTTP ${status}"
    else
        fail "GET http://localhost:3000${route} → HTTP ${status} (expected 200)"
    fi
done

# ── Summary ───────────────────────────────────────────────────────────────────
echo ""
echo "========================================================"
echo "  WORKFLOW VERIFICATION RESULTS"
echo "========================================================"
echo ""
echo "  Company registered: ${TEST_SLUG} (ID ${CID})"
echo "  Resources created:"
echo "    Branch ID:     ${BR_ID}"
echo "    Warehouse ID:  ${WH_ID}"
echo "    Customer ID:   ${CUST_ID}"
echo "    Supplier ID:   ${SUP_ID}"
echo "    Product ID:    ${PROD_ID}"
echo "    Quotation ID:  ${QT_ID}"
echo "    Order ID:      ${SO_ID}"
echo "    Invoice ID:    ${INV_ID}"
echo "    Movement ID:   ${MOV_ID}"
echo ""
echo -e "${GREEN}  PASSED: ${PASS_COUNT}${NC}"
if [[ "${FAIL_COUNT}" -gt 0 ]]; then
    echo -e "${RED}  FAILED: ${FAIL_COUNT}${NC}"
    exit 1
fi
echo ""
echo -e "${GREEN}========================================================"
echo -e "  ✓  END-TO-END WORKFLOW COMPLETE"
echo -e "  All ${STEP} steps executed successfully."
echo -e "  ${PASS_COUNT} assertions passed, ${FAIL_COUNT} failed."
echo -e "========================================================${NC}"
echo ""
