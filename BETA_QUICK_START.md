# MADAR Closed Beta — Quick Start Guide

**Version**: v1.0.0-beta  
**Date**: 2026-07-18  
**Time to First Login**: ~5 minutes

---

## Prerequisites

You need these installed on your machine before you begin:

| Tool | Version | Download |
|------|---------|----------|
| **Docker Desktop** | 24+ | https://docs.docker.com/get-docker/ |
| **Docker Compose** | v2 (bundled with Docker Desktop) | Included above |
| **Git** | Any | https://git-scm.com/downloads |
| **A modern browser** | Chrome 120+ or Firefox 120+ | — |

```bash
# Verify before starting
docker --version          # → Docker version 24.x.x
docker compose version    # → Docker Compose version v2.x.x
```

---

## Step 1 — Get the Code

```bash
git clone https://github.com/mdardash-star/MADAR.git
cd MADAR
```

---

## Step 2 — Configure Environment

Copy the environment template files. **No changes needed for local beta testing** — the defaults work as-is.

```bash
cp .env.example .env
cp apps/api/.env.example apps/api/.env
cp apps/web/.env.example apps/web/.env
```

---

## Step 3 — Start the Application

```bash
docker compose up --build -d
```

This builds and starts 4 Docker containers:
- **PostgreSQL** (database)
- **Redis** (caching)
- **FastAPI** (API server, port 8000)
- **Next.js** (web frontend, port 3000)

Wait ~60 seconds for all services to initialize. You can check progress with:

```bash
docker compose ps
```

All 4 services should show as **running** or **healthy**.

---

## Step 4 — Initialize the Database

```bash
# Apply database schema (run once after first start)
docker compose exec api alembic upgrade head
```

You should see output like:
```
INFO  Running upgrade  -> 20260718_000001, Initial schema
INFO  Running upgrade 20260718_000001 -> 20260718_000002, ...
...
INFO  Running upgrade 20260718_000013 -> 20260718_000014, ...
```

---

## Step 5 — Load Beta Demo Data

```bash
docker compose exec api sh -c "cd /app && PYTHONPATH=/app python scripts/beta_seed.py"
```

This creates the **Gulf Electronics & Trading Ltd** demo company with:
- 4 demo user accounts
- 3 branches, 4 warehouses
- 8 customers, 5 suppliers
- 15 products
- 6 quotations, 6 orders, 3 invoices, 13 stock movements

---

## Step 6 — Access MADAR

Open your browser and go to:

| Service | URL |
|---------|-----|
| **Web Application** | http://localhost:3000 |
| **API Documentation** | http://localhost:8000/docs |
| **System Health** | http://localhost:8000/health |

---

## Demo User Credentials

Use these accounts to test different roles:

| Role | Email | Password | Access Level |
|------|-------|----------|-------------|
| **System Administrator** | admin@gulf-trading.demo | BetaAdmin2026! | Full access |
| **Sales Manager** | sales@gulf-trading.demo | BetaSales2026! | Sales + customers |
| **Inventory Manager** | inventory@gulf-trading.demo | BetaInventory2026! | Warehouse + stock |
| **Accountant** | accountant@gulf-trading.demo | BetaAccount2026! | Finance + invoices |

---

## Testing Guide

Follow [USER_TEST_PLAN.md](USER_TEST_PLAN.md) for step-by-step test scenarios covering:

1. Login & Navigation
2. Dashboard overview
3. Branch & warehouse management
4. Customer management
5. Product catalog
6. Full sales workflow (quotation → order → invoice)
7. Inventory management
8. Role-based access

---

## Reporting Issues

| Type | How to Report |
|------|--------------|
| **Bug** | Fill in [BUG_REPORT_TEMPLATE.md](BUG_REPORT_TEMPLATE.md) → submit as GitHub Issue |
| **Feedback** | Fill in [BETA_FEEDBACK_TEMPLATE.md](BETA_FEEDBACK_TEMPLATE.md) → email or GitHub |
| **Urgent** | Email: beta@madar.app |

---

## Known Limitations

Before testing, review [KNOWN_LIMITATIONS.md](KNOWN_LIMITATIONS.md) for a list of known issues.

**Key limitations to know upfront:**
- No pagination in tables (all records load at once)
- No data export (CSV/PDF)
- UI does not enforce role permissions (API does)
- Customer/supplier codes are globally unique (use prefixes if you get duplicate errors)

---

## Stopping MADAR

```bash
# Stop all services (data preserved)
docker compose down

# Stop and delete all data (clean slate)
docker compose down -v
```

---

## Troubleshooting

### Port already in use

```bash
# If port 8000 or 3000 is in use, kill the occupying process:
lsof -ti:8000 | xargs kill -9 2>/dev/null
lsof -ti:3000 | xargs kill -9 2>/dev/null
# Then retry docker compose up -d
```

### API container not networking correctly

```bash
# If the API can't connect to the database:
docker network connect madar_default madar-api-1
docker compose exec api alembic upgrade head
```

### Reset everything and start fresh

```bash
docker compose down -v
docker compose up --build -d
docker compose exec api alembic upgrade head
docker compose exec api sh -c "cd /app && PYTHONPATH=/app python scripts/beta_seed.py"
```

---

## System Requirements

| Resource | Minimum | Recommended |
|----------|---------|-------------|
| RAM | 4 GB free | 8 GB free |
| Disk | 5 GB free | 10 GB free |
| CPU | 2 cores | 4 cores |
| OS | macOS 12+, Windows 10+, Ubuntu 22+ | Any modern OS |

---

*Thank you for participating in the MADAR closed beta. Your testing and feedback help us build a better product.*
