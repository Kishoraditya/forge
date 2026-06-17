# =============================================================================
# Forge — Developer Commands
# =============================================================================
# Usage: make <target>
# Run `make help` to see all available commands.
# =============================================================================

.PHONY: dev test lint spec task context flow format type-check audit help ci-check ci-contract ci-check-backend ci-check-frontend

## ---- Local Development ----

## Start all local services
dev:
	docker-compose -f infra/docker/docker-compose.dev.yml up

## Start all local services (detached)
dev-bg:
	docker-compose -f infra/docker/docker-compose.dev.yml up -d

## Stop all local services
stop:
	docker-compose -f infra/docker/docker-compose.dev.yml down

## Rebuild and start services
rebuild:
	docker-compose -f infra/docker/docker-compose.dev.yml up --build

## ---- Testing ----

## Run full test suite with HTML report
test:
	cd backend && poetry run pytest tests/ -v --html=../reports/test/report.html --self-contained-html

## Run unit tests only
test-unit:
	cd backend && poetry run pytest tests/unit/ -v

## Run integration tests only
test-integration:
	cd backend && poetry run pytest tests/integration/ -v

## Run tests with coverage report
test-cov:
	cd backend && poetry run pytest tests/ --cov=app --cov-report=html:../reports/test/coverage/ --cov-report=term

## ---- Code Quality ----

## Run linting + type check
lint:
	cd backend && poetry run ruff check . && poetry run mypy app/

## Auto-format code
format:
	cd backend && poetry run black . && poetry run isort . && poetry run ruff check --fix .

## Run type checking only
type-check:
	cd backend && poetry run mypy app/

## Run security audit
audit:
	cd backend && poetry run pip-audit

## Run all pre-commit hooks
pre-commit:
	pre-commit run --all-files

## ---- CI Parity (mirrors .github/workflows/ci.yml) ----

## Run CI contract tests only
ci-contract:
	poetry run pytest backend/tests/ci/ -v

## Backend CI checks
ci-check-backend:
	poetry run pytest backend/tests/unit/ -v
	cd backend && poetry run ruff check . && poetry run mypy app/

## Frontend CI checks
ci-check-frontend:
	cd frontend && npm ci && npm run lint && npm run build

## Full local CI parity check
ci-check: ci-contract ci-check-backend ci-check-frontend

## ---- Scaffolding ----

## Scaffold a new spec file (usage: make spec F=F001)
spec:
	bash scripts/create_spec.sh $(F)

## Scaffold a new task (interactive)
task:
	bash scripts/create_task.sh

## ---- Documentation ----

## Remind yourself to update CONTEXT.md
context:
	bash scripts/context_refresh.sh

## Show manual test flow for a feature (usage: make flow F=F009)
flow:
	@echo "Opening manual test guide for $(F)..."
	@grep -A 50 "## $(F)" docs/MANUAL_TESTING.md | head -50

## ---- Database ----

## Run Alembic migrations
migrate:
	cd backend && poetry run alembic upgrade head

## Create a new migration
migration:
	cd backend && poetry run alembic revision --autogenerate -m "$(MSG)"

## ---- Help ----

## Show this help message
help:
	@echo "Forge — Available Commands:"
	@echo ""
	@grep -E '^## ' Makefile | sed 's/## /  /'
	@echo ""
	@echo "Usage: make <target>"
