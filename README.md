# MADAR ERP SaaS

MADAR is a production-ready ERP SaaS monorepo built with a FastAPI backend, a Next.js + TypeScript + Tailwind frontend, PostgreSQL, SQLAlchemy, Alembic, Redis, Docker, and GitHub Actions CI.

## Overview

- Monorepo with isolated application packages.
- FastAPI REST API with JWT authentication, refresh tokens, login, company registration, and current-user endpoints.
- Next.js frontend using TypeScript and Tailwind CSS with RTL Arabic layout support.
- PostgreSQL database with Alembic-managed migrations.
- Multi-tenant ready architecture with company, branch, role, and permission models.
- Docker Compose for local development with PostgreSQL and Redis.
- GitHub Actions for CI validation.

## Repository Structure

- `apps/api` — FastAPI backend
- `apps/web` — Next.js frontend
- `docker-compose.yml` — local services orchestration
- `.github/workflows/ci.yml` — CI pipeline

## Prerequisites

- Docker
- Docker Compose
- Node.js 20+
- Python 3.12+
- npm

## Local Development

1. Copy environment files:
   ```bash
   cp .env.example .env
   cp apps/api/.env.example apps/api/.env
   cp apps/web/.env.example apps/web/.env
   ```

2. Start the full stack:
   ```bash
   docker compose up --build
   ```

3. Access the apps:
   - Frontend: http://localhost:3000
   - API docs: http://localhost:8000/docs
   - PostgreSQL: localhost:5432
   - Redis: localhost:6379

## Backend Setup

```bash
cd apps/api
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Frontend Setup

```bash
cd apps/web
npm install
npm run dev
```

## Database Migrations

```bash
cd apps/api
alembic upgrade head
```

## Phase 1 APIs

- `POST /auth/login` — login and receive access and refresh tokens
- `POST /auth/refresh` — exchange refresh token for a new session token pair
- `GET /auth/me` — retrieve authenticated user payload
- `POST /companies/register` — register a new company and bootstrap the first admin user
- `GET /api/v1/me` — current user endpoint for authenticated API clients

## Production Guidance

- Replace default secrets and credentials.
- Use a managed PostgreSQL and Redis service in production.
- Configure secure JWT secrets in environment variables.
- Enable reverse proxy TLS and a production-grade WAF in deployment.
- Use tenant-specific RBAC scopes and separate credentials per environment.
