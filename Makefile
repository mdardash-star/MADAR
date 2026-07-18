# MADAR Operations Makefile
# Usage: make <target>
# Run 'make help' for all available commands

.DEFAULT_GOAL := help
.PHONY: help

COMPOSE_DEV  = docker compose -f docker-compose.yml
COMPOSE_PROD = docker compose -f docker-compose.prod.yml
SHELL        = /bin/bash

# ─── Help ────────────────────────────────────────────────────────────────────

help: ## Show this help message
	@echo ""
	@echo "MADAR Operations Commands"
	@echo "========================="
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-28s\033[0m %s\n", $$1, $$2}'
	@echo ""

# ─── Development ─────────────────────────────────────────────────────────────

dev: ## Start full development stack
	$(COMPOSE_DEV) up --build -d
	@echo "  Frontend: http://localhost:3000"
	@echo "  API:      http://localhost:8000"
	@echo "  API Docs: http://localhost:8000/docs"

dev-logs: ## Tail all development logs
	$(COMPOSE_DEV) logs -f

dev-stop: ## Stop development stack
	$(COMPOSE_DEV) down

dev-reset: ## Reset development stack (removes volumes)
	$(COMPOSE_DEV) down -v
	@echo "⚠️  All data removed"

dev-shell-api: ## Open shell in API container (dev)
	$(COMPOSE_DEV) exec api bash

dev-shell-db: ## Open psql in database container (dev)
	$(COMPOSE_DEV) exec db psql -U madar madar

# ─── Testing ─────────────────────────────────────────────────────────────────

test: ## Run backend tests
	cd apps/api && . .venv/bin/activate && pytest tests/ -q

test-verbose: ## Run backend tests with verbose output
	cd apps/api && . .venv/bin/activate && pytest tests/ -v

test-e2e: ## Run only end-to-end workflow test
	cd apps/api && . .venv/bin/activate && pytest tests/test_workflow_e2e.py -v

test-coverage: ## Run tests with coverage report
	cd apps/api && . .venv/bin/activate && pytest tests/ --cov=app --cov-report=html
	@echo "Coverage report: apps/api/htmlcov/index.html"

lint: ## Run backend linter (ruff)
	cd apps/api && ruff check .

lint-fix: ## Auto-fix lint issues
	cd apps/api && ruff check --fix .

typecheck-web: ## Run TypeScript type check on frontend
	cd apps/web && npx tsc --noEmit

test-web: ## Build frontend (validates TypeScript)
	cd apps/web && npm run build

# ─── Database ────────────────────────────────────────────────────────────────

migrate: ## Apply database migrations (dev)
	$(COMPOSE_DEV) exec api alembic upgrade head

migrate-prod: ## Apply database migrations (production)
	$(COMPOSE_PROD) exec api alembic upgrade head

migrate-status: ## Show current migration status
	$(COMPOSE_DEV) exec api alembic current

migrate-history: ## Show migration history
	$(COMPOSE_DEV) exec api alembic history --verbose

migrate-rollback: ## Rollback last migration
	$(COMPOSE_DEV) exec api alembic downgrade -1

seed: ## Seed sample data (dev)
	$(COMPOSE_DEV) exec api sh -c "cd /app && PYTHONPATH=/app python scripts/seed_sample_data.py"

seed-prod: ## Seed sample data (production — use with caution)
	@echo "⚠️  About to seed sample data in PRODUCTION"
	@read -p "Press ENTER to continue or CTRL+C to cancel..."
	$(COMPOSE_PROD) exec api sh -c "cd /app && PYTHONPATH=/app python scripts/seed_sample_data.py"

# ─── Production ──────────────────────────────────────────────────────────────

prod-up: ## Start production stack
	$(COMPOSE_PROD) up -d
	@echo "Waiting for services..."
	@sleep 10
	@$(COMPOSE_PROD) ps

prod-build: ## Build production images
	$(COMPOSE_PROD) build

prod-deploy: ## Full production deploy (build + up + migrate)
	@echo "🚀 Deploying MADAR to production..."
	$(COMPOSE_PROD) build
	$(COMPOSE_PROD) up -d --no-deps api
	@sleep 10
	$(MAKE) migrate-prod
	$(COMPOSE_PROD) up -d --no-deps web
	@sleep 5
	$(MAKE) health-prod
	@echo "✅ Deployment complete"

prod-down: ## Stop production stack
	$(COMPOSE_PROD) down

prod-logs: ## Tail production logs
	$(COMPOSE_PROD) logs -f

prod-logs-api: ## Tail API logs only (production)
	$(COMPOSE_PROD) logs -f api

prod-status: ## Show production service status
	$(COMPOSE_PROD) ps

prod-restart-api: ## Restart only the API container (zero-downtime)
	$(COMPOSE_PROD) restart api
	@sleep 5
	$(MAKE) health-prod

prod-shell-api: ## Open shell in production API container
	$(COMPOSE_PROD) exec api bash

prod-shell-db: ## Open psql in production database
	$(COMPOSE_PROD) exec db psql -U $$POSTGRES_USER $$POSTGRES_DB

# ─── Health & Monitoring ─────────────────────────────────────────────────────

health: ## Check API health (dev)
	@curl -sf http://localhost:8000/health && echo " ✅ healthy" || echo " ❌ unhealthy"

health-ready: ## Check API readiness (dev)
	@curl -s http://localhost:8000/health/ready | python3 -m json.tool

health-prod: ## Check production health
	@curl -sf https://app.madar.app/health && echo " ✅ prod healthy" || echo " ❌ prod unhealthy"

metrics: ## Show API metrics (dev)
	@curl -s http://localhost:8000/metrics | grep "^http_requests_total" | head -20

grafana: ## Open Grafana via SSH tunnel (prod)
	@echo "Opening Grafana tunnel on localhost:3001"
	@echo "Press CTRL+C to close"
	ssh -L 3001:localhost:3001 ubuntu@$${PROD_HOST} -N

prometheus: ## Open Prometheus via SSH tunnel (prod)
	@echo "Opening Prometheus tunnel on localhost:9090"
	ssh -L 9090:localhost:9090 ubuntu@$${PROD_HOST} -N

# ─── Backup ──────────────────────────────────────────────────────────────────

backup: ## Run database backup (production)
	bash scripts/backup.sh

backup-list: ## List available backups
	@echo "=== Local Backups ==="
	@ls -lth backups/*.dump 2>/dev/null | head -10 || echo "  (none)"
	@echo ""
	@echo "=== S3 Backups ==="
	@aws s3 ls $${S3_BACKUP_BUCKET}/daily/ 2>/dev/null | sort -r | head -10 || echo "  (S3 not configured)"

restore: ## Restore database (interactive)
	bash scripts/restore.sh

restore-from: ## Restore from specific file: make restore-from FILE=backups/xxx.dump
	bash scripts/restore.sh $(FILE)

# ─── SSL Certificates ────────────────────────────────────────────────────────

ssl-init: ## Initialize SSL certificates (first time)
	docker compose -f docker-compose.prod.yml run --rm certbot \
		certbot certonly --webroot \
		-w /var/www/certbot \
		-d $${DOMAIN} \
		--email $${CERTBOT_EMAIL} \
		--agree-tos --no-eff-email

ssl-renew: ## Manually renew SSL certificates
	docker compose -f docker-compose.prod.yml run --rm certbot certbot renew
	$(COMPOSE_PROD) restart nginx

ssl-check: ## Check SSL certificate expiry
	@echo | openssl s_client -servername $${DOMAIN:-app.madar.app} \
		-connect $${DOMAIN:-app.madar.app}:443 2>/dev/null \
		| openssl x509 -noout -dates 2>/dev/null \
		|| echo "Could not connect — is the domain live?"

# ─── Secrets ─────────────────────────────────────────────────────────────────

gen-jwt-secret: ## Generate a new JWT secret
	@openssl rand -hex 32

gen-password: ## Generate a strong password
	@openssl rand -base64 24

secrets-check: ## Verify no default secrets in production env
	@if grep -q "CHANGE_ME" .env.production 2>/dev/null; then \
		echo "❌ .env.production still has CHANGE_ME placeholders!"; exit 1; \
	else echo "✅ No default secrets found"; fi

# ─── Cleanup ──────────────────────────────────────────────────────────────────

clean-docker: ## Remove unused Docker resources
	docker system prune -f
	docker image prune -f

clean-old-images: ## Remove old Docker images (keep last 3)
	docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.ID}}" \
		| grep madar | tail -n +4 | awk '{print $$3}' | xargs docker rmi -f 2>/dev/null || true

clean-backups: ## Remove local backups older than 7 days
	find backups/ -name "*.dump" -mtime +7 -delete 2>/dev/null && echo "✅ Old backups removed" || echo "No backups to clean"

# ─── Release ─────────────────────────────────────────────────────────────────

release-rc: ## Create a release candidate tag
	@read -p "Enter RC version (e.g., v1.0.0-rc2): " VERSION; \
	git tag -a "$$VERSION" -m "Release Candidate: $$VERSION"; \
	echo "✅ Tagged $$VERSION — push with: git push origin $$VERSION"

release-stable: ## Create a stable release tag
	@read -p "Enter stable version (e.g., v1.0.0): " VERSION; \
	git tag -a "$$VERSION" -m "Stable release: $$VERSION"; \
	echo "✅ Tagged $$VERSION — push with: git push origin $$VERSION"
