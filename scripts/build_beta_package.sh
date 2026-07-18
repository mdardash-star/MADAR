#!/usr/bin/env bash
# ============================================================
# MADAR Closed Beta — Deployment Package Builder
# ============================================================
# Creates a self-contained deployment archive for beta testers
# that includes everything needed to run MADAR locally.
#
# Usage:
#   bash scripts/build_beta_package.sh
#
# Output:
#   madar-beta-v1.0.0-YYYYMMDD.tar.gz
#   madar-beta-v1.0.0-YYYYMMDD/
#     ├── docker-compose.yml
#     ├── .env.example
#     ├── apps/api/.env.example
#     ├── apps/web/.env.example
#     ├── BETA_QUICK_START.md
#     ├── USER_TEST_PLAN.md
#     ├── BUG_REPORT_TEMPLATE.md
#     └── BETA_FEEDBACK_TEMPLATE.md

set -euo pipefail

VERSION="v1.0.0-beta"
DATE=$(date +"%Y%m%d")
PKG_NAME="madar-beta-${VERSION}-${DATE}"
PKG_DIR="/tmp/${PKG_NAME}"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "Building MADAR beta deployment package..."
echo "  Version: ${VERSION}"
echo "  Package: ${PKG_NAME}"
echo ""

# Clean and create package directory
rm -rf "${PKG_DIR}"
mkdir -p "${PKG_DIR}"

# ── Core deployment files ────────────────────────────────────────────────────
cp "${REPO_ROOT}/docker-compose.yml"               "${PKG_DIR}/"
cp "${REPO_ROOT}/.env.example"                     "${PKG_DIR}/"
cp "${REPO_ROOT}/apps/api/.env.example"            "${PKG_DIR}/api.env.example"
cp "${REPO_ROOT}/apps/web/.env.example"            "${PKG_DIR}/web.env.example"

# ── Beta documentation ───────────────────────────────────────────────────────
cp "${REPO_ROOT}/USER_TEST_PLAN.md"                "${PKG_DIR}/"
cp "${REPO_ROOT}/BUG_REPORT_TEMPLATE.md"           "${PKG_DIR}/"
cp "${REPO_ROOT}/BETA_FEEDBACK_TEMPLATE.md"        "${PKG_DIR}/"
cp "${REPO_ROOT}/KNOWN_LIMITATIONS.md"             "${PKG_DIR}/"

# ── Quick start guide (beta-specific) ───────────────────────────────────────
cat > "${PKG_DIR}/BETA_QUICK_START.md" << 'QUICKSTART'
# MADAR Closed Beta — Quick Start Guide

**Version**: v1.0.0-beta  
**Time to First Login**: ~5 minutes

---

## Prerequisites

Ensure you have these installed before starting:

| Tool | Version | Download |
|------|---------|---------|
| Docker | 24+ | https://docs.docker.com/get-docker/ |
| Docker Compose | v2 | Included with Docker Desktop |
| A modern browser | Chrome/Firefox | — |

Verify installation:
```bash
docker --version
docker compose version
```

---

## Step 1 — Configure Environment

```bash
# Copy environment files
cp .env.example .env
cp api.env.example apps/api/.env
cp web.env.example apps/web/.env
```

No changes needed for local beta testing — defaults work out of the box.

---

## Step 2 — Start MADAR

```bash
docker compose up --build -d
```

Wait ~60 seconds for all services to initialize. Progress:
```bash
docker compose ps   # should show all 4 services running
```

---

## Step 3 — Initialize Database

```bash
# Apply database schema
docker compose exec api alembic upgrade head

# Load beta demo data (Gulf Electronics & Trading Ltd)
docker compose exec api sh -c "cd /app && PYTHONPATH=/app python scripts/beta_seed.py"
```

---

## Step 4 — Access MADAR

| Service | URL | Notes |
|---------|-----|-------|
| **Web App** | http://localhost:3000 | Start here |
| **API Docs** | http://localhost:8000/docs | Interactive API explorer |
| **Health Check** | http://localhost:8000/health | Should return `{"status":"healthy"}` |

---

## Demo Credentials

| Role | Email | Password |
|------|-------|---------|
| System Administrator | admin@gulf-trading.demo | BetaAdmin2026! |
| Sales Manager | sales@gulf-trading.demo | BetaSales2026! |
| Inventory Manager | inventory@gulf-trading.demo | BetaInventory2026! |
| Accountant | accountant@gulf-trading.demo | BetaAccount2026! |

---

## Testing Guide

Follow the **USER_TEST_PLAN.md** for step-by-step test scenarios.

---

## Stopping MADAR

```bash
# Stop (preserves data)
docker compose down

# Stop and reset all data
docker compose down -v
```

---

## Reporting Issues

- **Bugs**: Use **BUG_REPORT_TEMPLATE.md** → submit via GitHub Issues
- **Feedback**: Use **BETA_FEEDBACK_TEMPLATE.md** → email or GitHub
- **Contact**: beta@madar.app

QUICKSTART

# ── Package information ──────────────────────────────────────────────────────
cat > "${PKG_DIR}/README_BETA.md" << README
# MADAR Closed Beta — v1.0.0-beta

**Date**: $(date +"%Y-%m-%d")  
**Status**: Closed Beta  
**Company**: Gulf Electronics & Trading Ltd (pre-loaded demo)

## Files in This Package

| File | Purpose |
|------|---------|
| docker-compose.yml | Container orchestration |
| .env.example | Root environment template |
| api.env.example | API service environment template |
| web.env.example | Frontend environment template |
| BETA_QUICK_START.md | Setup and login instructions |
| USER_TEST_PLAN.md | Test scenarios to follow |
| BUG_REPORT_TEMPLATE.md | Template for reporting bugs |
| BETA_FEEDBACK_TEMPLATE.md | Template for general feedback |
| KNOWN_LIMITATIONS.md | Known issues and limitations |

## Quick Start

```bash
cp .env.example .env && cp api.env.example apps/api/.env && cp web.env.example apps/web/.env
docker compose up --build -d
docker compose exec api alembic upgrade head
docker compose exec api sh -c "cd /app && PYTHONPATH=/app python scripts/beta_seed.py"
# Open http://localhost:3000
```

## Demo Login

- Email: admin@gulf-trading.demo
- Password: BetaAdmin2026!
README

# ── Create archive ───────────────────────────────────────────────────────────
ARCHIVE="${REPO_ROOT}/${PKG_NAME}.tar.gz"
tar -czf "${ARCHIVE}" -C /tmp "${PKG_NAME}"
ARCHIVE_SIZE=$(du -sh "${ARCHIVE}" | cut -f1)

echo "✅  Package built: ${ARCHIVE} (${ARCHIVE_SIZE})"
echo ""
echo "Contents:"
ls -la "${PKG_DIR}/"
echo ""
echo "To distribute: share ${PKG_NAME}.tar.gz with beta testers"
