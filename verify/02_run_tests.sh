#!/usr/bin/env bash
# ===========================================================================
# verify/02_run_tests.sh
# Runs the complete automated test suite (backend pytest).
# Requires the API service to be running with a connected database.
#
# Exit codes:
#   0 = all tests passed
#   1 = test failure or setup error
# ===========================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "${SCRIPT_DIR}")"
API_DIR="${PROJECT_DIR}/apps/api"

GREEN='\033[0;32m'; RED='\033[0;31m'; YELLOW='\033[1;33m'; NC='\033[0m'
ok()   { echo -e "${GREEN}  ✓${NC}  $*"; }
fail() { echo -e "${RED}  ✗${NC}  $*"; exit 1; }
info() { echo -e "${YELLOW}  ▶${NC}  $*"; }

echo ""
echo "========================================================"
echo "  MADAR — Automated Test Suite"
echo "  $(date -Iseconds)"
echo "========================================================"

# ── Check Python environment ──────────────────────────────────────────────────
info "Locating Python environment..."
if [[ -f "${API_DIR}/.venv/bin/activate" ]]; then
    ACTIVATE="${API_DIR}/.venv/bin/activate"
    ok "Found virtual environment at ${API_DIR}/.venv"
elif command -v python3 >/dev/null 2>&1; then
    ACTIVATE=""
    ok "Using system Python: $(python3 --version)"
else
    fail "No Python environment found"
fi

# ── Verify API is reachable ───────────────────────────────────────────────────
info "Checking API is healthy before running tests..."
curl -sf http://localhost:8000/health >/dev/null 2>&1 || \
    fail "API is not healthy at http://localhost:8000/health — run 01_start_clean.sh first"
ok "API is healthy"

# ── Run tests ─────────────────────────────────────────────────────────────────
info "Running pytest from ${API_DIR}..."
echo ""

RUN_CMD="cd '${API_DIR}'"
if [[ -n "${ACTIVATE}" ]]; then
    RUN_CMD="${RUN_CMD} && source '${ACTIVATE}'"
fi
RUN_CMD="${RUN_CMD} && pytest tests/ -v --tb=short 2>&1"

TEST_OUTPUT=$(eval "${RUN_CMD}") || true

echo "${TEST_OUTPUT}"
echo ""

# ── Parse results ─────────────────────────────────────────────────────────────
PASSED=$(echo "${TEST_OUTPUT}" | grep -oE '[0-9]+ passed' | head -1 || echo "0 passed")
FAILED=$(echo "${TEST_OUTPUT}" | grep -oE '[0-9]+ failed' | head -1 || echo "")
ERRORS=$(echo "${TEST_OUTPUT}" | grep -oE '[0-9]+ error[^s]'  | head -1 || echo "")
WARNINGS=$(echo "${TEST_OUTPUT}" | grep -oE '[0-9]+ warning' | head -1 || echo "")

echo "========================================================"
echo "  TEST RESULTS"
echo "========================================================"
ok "Passed:   ${PASSED}"
[[ -n "${FAILED}" ]]   && echo -e "${RED}  ✗  Failed:   ${FAILED}${NC}"
[[ -n "${ERRORS}" ]]   && echo -e "${RED}  ✗  Errors:   ${ERRORS}${NC}"
[[ -n "${WARNINGS}" ]] && echo "     Warnings: ${WARNINGS}"

# ── Final verdict ─────────────────────────────────────────────────────────────
PASSED_NUM=$(echo "${PASSED}" | grep -oE '[0-9]+' || echo "0")
if [[ "${PASSED_NUM}" -gt 0 ]]; then
    if [[ -n "${FAILED}" || -n "${ERRORS}" ]]; then
        fail "Test suite completed with failures — ${FAILED} ${ERRORS}"
    fi
    echo ""
    echo -e "${GREEN}========================================================"
    echo -e "  ✓  TEST SUITE PASSED — ${PASSED}"
    echo -e "========================================================${NC}"
    echo ""
else
    fail "Test suite did not complete successfully — check output above"
fi
