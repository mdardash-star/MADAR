# MADAR ERP SaaS — Installation Guide

**Version**: v0.1  
**Updated**: 2026-07-18

---

## Table of contents

1. [Prerequisites](#prerequisites)
2. [Repository setup](#repository-setup)
3. [Environment configuration](#environment-configuration)
4. [Option A — Docker Compose (recommended)](#option-a--docker-compose-recommended)
5. [Option B — Local development without Docker](#option-b--local-development-without-docker)
6. [Database migrations](#database-migrations)
7. [Verify the installation](#verify-the-installation)
8. [Production checklist](#production-checklist)

---

## Prerequisites

| Tool | Minimum version | Notes |
|------|----------------|-------|
| Git | Any | Clone the repository |
| Docker | 24+ | For Docker Compose option |
| Docker Compose | v2 (`docker compose`) | Bundled with Docker Desktop |
| Python | 3.12+ | Local dev only |
| Node.js | 20+ | Local dev only |
| PostgreSQL | 16+ | Provided by Docker or managed service |
| Redis | 7+ | Provided by Docker or managed service |

---

## Repository setup

```bash
git clone https://github.com/mdardash-star/MADAR.git
cd MADAR
```

---

## Environment configuration

Copy the example environment files. You **must** do this before any other step.

```bash
# Root environment (used by Docker Compose)
cp .env.example .env

# Backend environment
cp apps/api/.env.example apps/api/.env

# Frontend environment
cp apps/web/.env.example apps/web/.env   # if it exists
```

**Required secrets to change before production** (edit `.env` and `apps/api/.env`):

| Variable | Default | Action |
|----------|---------|--------|
| `JWT_SECRET_KEY` | `change-this-secret-key-in-production` | **Must change** — use a 64-char random string |
| `POSTGRES_PASSWORD` | `madar_password` | Change to a strong password |
| `POSTGRES_USER` | `madar` | Optional |
| `POSTGRES_DB` | `madar` | Optional |

Generate a secure JWT secret:
```bash
openssl rand -hex 32
```

---

## Option A — Docker Compose (recommended)

This starts all four services (database, Redis, API, web) in one command.

```bash
# Build images and start all services
docker compose up --build

# Or in detached mode
docker compose up --build -d
```

Wait for all services to be healthy, then run migrations:

```bash
# Run database migrations (first time only, or after schema changes)
docker compose exec api alembic upgrade head
```

**Optional: Load sample demo data:**

```bash
docker compose exec api sh -c "cd /app && PYTHONPATH=/app python scripts/seed_sample_data.py"
# Demo credentials: admin@acme-demo.com / Demo123!
```

**Service URLs:**

| Service | URL |
|---------|-----|
| Frontend | http://localhost:3000 |
| API | http://localhost:8000 |
| API docs (Swagger) | http://localhost:8000/docs |
| API docs (ReDoc) | http://localhost:8000/redoc |
| PostgreSQL | localhost:5432 |
| Redis | localhost:6379 |

**Stop all services:**

```bash
docker compose down
```

**Stop and remove volumes (full reset):**

```bash
docker compose down -v
```

---

## Option B — Local development without Docker

Requires PostgreSQL and Redis to be running locally.

### Backend

```bash
cd apps/api

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure .env to point at your local PostgreSQL/Redis
# (edit POSTGRES_HOST=localhost, REDIS_HOST=localhost)

# Run the API server
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd apps/web

# Install dependencies
npm install

# Start the development server
npm run dev
```

Frontend will be available at http://localhost:3000.

---

## Database migrations

Alembic manages all schema changes. Always run migrations after pulling new code.

```bash
# Docker Compose
docker compose exec api alembic upgrade head

# Local development
cd apps/api
source .venv/bin/activate
alembic upgrade head
```

Check the current migration version:
```bash
alembic current
```

View migration history:
```bash
alembic history --verbose
```

---

## Verify the installation

After starting all services and running migrations, confirm the stack is healthy:

```bash
# Health check
curl http://localhost:8000/health
# Expected: {"status":"healthy"}

# API root
curl http://localhost:8000/
# Expected: {"name":"MADAR ERP API","status":"ok","environment":"development"}

# API version status
curl http://localhost:8000/api/v1/status
# Expected: {"status":"ok"}
```

Run the automated test suite (local dev only):

```bash
cd apps/api
source .venv/bin/activate
pytest -q
# Expected: 48 passed, 0 failed
```

---

## Production checklist

Before going to production, complete every item in this checklist:

- [ ] `JWT_SECRET_KEY` changed to a 64-char+ random string
- [ ] `POSTGRES_PASSWORD` changed to a strong unique password
- [ ] Database hosted on a managed service (AWS RDS, Azure Database, etc.)
- [ ] Redis hosted on a managed service (ElastiCache, Redis Cloud, etc.)
- [ ] TLS/HTTPS enabled on the API and frontend via a reverse proxy (nginx, Caddy, AWS ALB)
- [ ] `CORS allow_origins` in `apps/api/app/main.py` restricted to your domain(s)
- [ ] `DEBUG=false` in production `.env`
- [ ] `APP_ENV=production` in production `.env`
- [ ] Container images built with `--no-cache` for a clean production image
- [ ] Secrets managed via a secrets manager (AWS Secrets Manager, Vault, etc.) — **never store in `.env` files in git**
- [ ] Automated backups configured for PostgreSQL
- [ ] Health check endpoints monitored (e.g. UptimeRobot, Datadog)
- [ ] Rate limiting configured on the API
- [ ] WAF configured in front of the application

---

## Troubleshooting

### `docker compose up` fails with "port already in use"
Stop any existing PostgreSQL or Redis instances on ports 5432 or 6379, or change the port mapping in `docker-compose.yml`.

### `alembic upgrade head` fails with "relation does not exist"
Ensure the database user has `CREATE TABLE` privileges on the target database:
```sql
GRANT ALL PRIVILEGES ON DATABASE madar TO madar;
```

### Backend fails to start with "password cannot be longer than 72 bytes"
Your bcrypt library version is incompatible with passlib. This project uses direct `bcrypt` calls — ensure `bcrypt>=4.0.0` is installed and there is no `passlib` import in `app/core/security.py`.

### Login returns 401 for a freshly created account
Ensure `alembic upgrade head` was run after all migrations. Check the `users` table has `hashed_password` populated.
