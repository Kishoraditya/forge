# F001 — Project Scaffolding & Monorepo
<!-- Spec version: 1.0.0 | Author: cursor | Date: 2026-06-17 -->

## Feature Reference
- **Feature ID**: F001
- **Phase**: Phase 0
- **Depends on**: none
- **Blocks**: F008, F002, F003, F004, F005, F006, F007
- **Feature registry entry**: docs/FEATURES.md
- **Estimated tasks**: 12

## What This Does (One Paragraph)
Establishes the runnable Forge monorepo skeleton: FastAPI backend with health
check, structured logging, settings loading, shared exceptions, test harness,
Docker Compose local dev stack (backend, frontend, Redis, Neo4j), and Alembic
migration bootstrap. Developers can run `make test`, `make lint`, and `make dev`
against a consistent local environment.

## What This Does NOT Do
- Business features (sessions, LLM, BYOK, RAG)
- Supabase table DDL (F008)
- Production deployment or Terraform
- CI secrets or hosted service wiring

## Acceptance Criteria
- [ ] AC1: `GET /health` returns `200` with `{"status":"ok"}` and correlation ID header
- [ ] AC2: Settings load from `.env.local` via Pydantic Settings with validation errors on missing required vars for boot
- [ ] AC3: Structlog configured per `docs/LOGGING.md` with correlation ID middleware
- [ ] AC4: `make test-unit` passes with at least health and config tests
- [ ] AC5: `make lint` passes on `backend/app/`
- [ ] AC6: `docker compose -f infra/docker/docker-compose.dev.yml config` validates
- [ ] AC7: `make dev` starts backend (:8000), frontend (:3000), Redis, Neo4j containers
- [ ] AC8: Alembic initialized under `backend/` with empty baseline migration

## Data Model
`Settings` (Pydantic Settings): `environment`, `debug`, `redis_url`, `neo4j_uri`,
`neo4j_username`, `neo4j_password`, `supabase_url`, `supabase_anon_key`,
`supabase_service_role_key` — loaded from env; secrets never logged.

`HealthResponse`: `{ "status": "ok", "environment": str }`

## Agent State Impact
None in Phase 0 scaffold.

## API Contract
`GET /health`
- Response 200: `{ "status": "ok", "environment": "development" }`
- Headers: `X-Correlation-ID: <uuid>`

## Files to Create
| File | Type | Purpose |
|------|------|---------|
| `backend/app/__init__.py` | New | Package marker |
| `backend/app/config.py` | New | Pydantic Settings |
| `backend/app/main.py` | New | FastAPI app factory |
| `backend/app/core/__init__.py` | New | Core package |
| `backend/app/core/exceptions.py` | New | Base app exceptions |
| `backend/app/core/logging.py` | New | Structlog setup |
| `backend/app/core/middleware.py` | New | Correlation ID middleware |
| `backend/app/api/__init__.py` | New | API package |
| `backend/app/api/health.py` | New | Health router |
| `backend/app/constants.py` | New | App-wide constants |
| `backend/tests/conftest.py` | New | Pytest fixtures |
| `backend/tests/unit/test_config.py` | New | Settings tests |
| `backend/tests/unit/test_health.py` | New | Health handler tests |
| `backend/tests/integration/test_health_api.py` | New | API integration test |
| `infra/docker/docker-compose.dev.yml` | New | Local dev stack |
| `infra/docker/Dockerfile.backend` | New | Backend image |
| `infra/docker/Dockerfile.frontend` | New | Frontend dev image |
| `backend/alembic.ini` | New | Alembic config |
| `backend/alembic/env.py` | New | Alembic env |
| `backend/alembic/versions/001_baseline.py` | New | Empty baseline |

## Files to Modify
| File | Change |
|------|--------|
| `Makefile` | Ensure targets work on Windows-friendly paths where needed |
| `pyproject.toml` | Add `structlog` if not present |

## Security & Secrets
Settings read secrets from environment only. Logging must redact per
`docs/SECURITY.md`. Health endpoint exposes no secrets.

## Dependencies
- `structlog` — structured logging (see `docs/LOGGING.md`)
- Alternatives: stdlib logging — rejected (no structured JSON)

## Test Cases
### Happy Path
- Settings with valid `.env` → app starts, `/health` returns 200

### Edge Cases
- Missing `ENVIRONMENT` → validation error at startup
- Invalid Redis URL format → validation error

### Should Not Happen
- API keys appearing in logs or health response

## Manual Test Flow
1. `make dev`
2. `curl http://localhost:8000/health` → 200 OK
3. Open `http://localhost:3000` → Next.js loads

## Phase/Feature Exit Signal
`make test-unit` and `make lint` green; `make dev` brings up four services.

## Notes & Assumptions
- Next.js 16 in frontend is accepted; update README stack note
- Python 3.11–3.13 supported; document `poetry env use 3.13`
- Supabase not in Docker; use hosted dev project from HT-007
