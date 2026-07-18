#!/usr/bin/env bash
# ===========================================================================
# verify/run_all.sh
# Master verification runner.
# Executes all 5 verification scripts in sequence and produces a final report.
#
# Usage:
#   bash verify/run_all.sh              # Full clean run (tears down everything)
#   bash verify/run_all.sh --skip-start # Skip 01_start_clean.sh (use existing stack)
#
# Exit codes:
#   0 = all scripts passed
#   1 = one or more scripts failed
# ===========================================================================
set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKIP_START="${1:-}"

GREEN='\033[0;32m'; RED='\033[0;31m'; YELLOW='\033[1;33m'; BOLD='\033[1m'; NC='\033[0m'

PASS_SCRIPTS=(); FAIL_SCRIPTS=()

run_script() {
    local num="$1" name="$2" file="${SCRIPT_DIR}/$3"
    echo ""
    echo -e "${YELLOW}${BOLD}================================================================${NC}"
    echo -e "${YELLOW}${BOLD}  Running ${num}: ${name}${NC}"
    echo -e "${YELLOW}${BOLD}================================================================${NC}"

    local start_time end_time elapsed exit_code=0
    start_time=$(date +%s)
    bash "${file}" || exit_code=$?
    end_time=$(date +%s)
    elapsed=$(( end_time - start_time ))

    if [[ ${exit_code} -eq 0 ]]; then
        echo -e "${GREEN}  ✓  ${num} PASSED in ${elapsed}s${NC}"
        PASS_SCRIPTS+=("${num}: ${name}")
    else
        echo -e "${RED}  ✗  ${num} FAILED (exit code ${exit_code}) in ${elapsed}s${NC}"
        FAIL_SCRIPTS+=("${num}: ${name}")
    fi
}

echo ""
echo -e "${BOLD}================================================================"
echo -e "  MADAR — Full Verification Suite"
echo -e "  $(date -Iseconds)"
echo -e "================================================================${NC}"

TOTAL_START=$(date +%s)

if [[ "${SKIP_START}" == "--skip-start" ]]; then
    echo -e "${YELLOW}  ⚑  Skipping 01_start_clean.sh (--skip-start flag set)${NC}"
    echo -e "${YELLOW}     Using existing Docker stack${NC}"
else
    run_script "01" "Clean Start"        "01_start_clean.sh"
fi

run_script "02" "Automated Tests"       "02_run_tests.sh"
run_script "03" "Demo Data Seeding"     "03_seed_demo.sh"
run_script "04" "API Smoke Tests"       "04_smoke_tests.sh"
run_script "05" "Browser Workflow"      "05_browser_workflow.sh"

TOTAL_END=$(date +%s)
TOTAL_ELAPSED=$(( TOTAL_END - TOTAL_START ))

echo ""
echo -e "${BOLD}================================================================"
echo -e "  VERIFICATION REPORT"
echo -e "  Total time: ${TOTAL_ELAPSED}s"
echo -e "================================================================${NC}"
echo ""

for s in "${PASS_SCRIPTS[@]}"; do
    echo -e "${GREEN}  ✓  ${s}${NC}"
done
for s in "${FAIL_SCRIPTS[@]}"; do
    echo -e "${RED}  ✗  ${s}${NC}"
done

echo ""
PASS_COUNT=${#PASS_SCRIPTS[@]}
FAIL_COUNT=${#FAIL_SCRIPTS[@]}

if [[ ${FAIL_COUNT} -eq 0 ]]; then
    echo -e "${GREEN}${BOLD}================================================================"
    echo -e "  ✓  ALL ${PASS_COUNT} VERIFICATION SCRIPTS PASSED"
    echo -e "  MADAR is fully operational."
    echo -e "================================================================${NC}"
    echo ""
    exit 0
else
    echo -e "${RED}${BOLD}================================================================"
    echo -e "  ✗  ${FAIL_COUNT} of $((PASS_COUNT + FAIL_COUNT)) SCRIPTS FAILED"
    echo -e "================================================================${NC}"
    echo ""
    exit 1
fi
