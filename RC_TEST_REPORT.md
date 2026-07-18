# MADAR Release Candidate Test Report

Date: 2026-07-18
Branch: main
Execution mode: RC validation (stabilization only)

## Test executions

### 1) Baseline full verification

Command:

bash verify/run_all.sh

Result:

- 01 Clean Start: PASS
- 02 Automated Tests: PASS
- 03 Demo Data Seeding: PASS
- 04 API Smoke Tests: PASS
- 05 Browser Workflow: PASS

Baseline details:

- Automated tests: 49 passed, 259 warnings
- Browser workflow: 36 assertions passed, 0 failed

### 2) Focused regression suite after fixes

Command:

cd apps/api && . .venv/bin/activate && pytest tests/test_release_v01.py -q

Result:

- 19 passed

### 3) Post-fix release verification

Command:

bash verify/run_all.sh --skip-start

Result:

- 02 Automated Tests: PASS
- 03 Demo Data Seeding: PASS
- 04 API Smoke Tests: PASS
- 05 Browser Workflow: PASS

Post-fix details:

- Automated tests: 50 passed, 0 warnings
- Smoke tests: 56 passed
- Browser workflow: 36 assertions passed, 0 failed

## Acceptance criteria status

- No Critical issues: PASS
- No High severity issues: PASS
- All acceptance tests passing: PASS
- All release gates passing: PASS

## Notes

- One stabilization bug was fixed (deprecated UTC timestamp API usage).
- New automated regression test added to prevent reintroduction.
- No new features were introduced in this RC cycle.
