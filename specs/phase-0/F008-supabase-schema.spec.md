# F008 — Supabase Schema Foundation
<!-- Spec version: 1.0.0 | Author: cursor | Date: 2026-06-17 -->

## Feature Reference
- **Feature ID**: F008
- **Phase**: Phase 0
- **Depends on**: F001
- **Blocks**: F002, F004, F006, F007
- **Feature registry entry**: docs/FEATURES.md
- **Estimated tasks**: 10

## What This Does (One Paragraph)
Defines and migrates the core PostgreSQL schema in Supabase: all Phase 0 tables
with indexes, pgvector column for embeddings, Alembic migrations, SQLAlchemy
async models, and RLS policies separating admin full access from anonymous
session-scoped read where applicable.

## What This Does NOT Do
- Neo4j graph schema (Phase 1 F009/F031)
- Seed data beyond admin config defaults
- Production Supabase branching

## Acceptance Criteria
- [ ] AC1: Tables exist: `sessions`, `messages`, `tools`, `skills`, `personalities`, `prompts`, `decisions`, `graph_nodes`, `graph_edges`, `api_keys`, `credit_ledger`, `feature_flags`, `documents`, `document_chunks`
- [ ] AC2: `CREATE EXTENSION IF NOT EXISTS vector` applied in migration
- [ ] AC3: `make migrate` applies all migrations on clean dev DB
- [ ] AC4: SQLAlchemy async models in `backend/app/models/` match schema
- [ ] AC5: RLS enabled; admin role full access; public policies scope by `session_id` where defined
- [ ] AC6: Repository layer in `backend/app/db/` — no raw SQL outside db layer
- [ ] AC7: Unit tests for model validation and migration smoke test

## Data Model
Core tables (abbreviated):

**sessions**: `id UUID PK`, `created_at`, `updated_at`, `status`, `model_alias`,
`token_count`, `budget_usd`, `budget_remaining_usd`, `expires_at`

**messages**: `id`, `session_id FK`, `role`, `content`, `token_count`, `created_at`

**api_keys**: `id`, `provider`, `encrypted_key`, `is_active`, `created_at`, `updated_at`

**credit_ledger**: `id`, `session_id FK`, `amount_usd`, `reason`, `created_at`

**document_chunks**: `id`, `document_id FK`, `content`, `embedding vector(1536)`, `metadata JSONB`

(Full column lists in migration files.)

## Agent State Impact
Persists `session_id`, messages, decisions — owners per `docs/STATE.md`.

## API Contract
None directly; consumed by services in F002/F004/F007.

## Files to Create
| File | Type | Purpose |
|------|------|---------|
| `backend/app/db/__init__.py` | New | DB package |
| `backend/app/db/session.py` | New | Async engine/session factory |
| `backend/app/db/base.py` | New | SQLAlchemy declarative base |
| `backend/app/models/__init__.py` | New | Model exports |
| `backend/app/models/session.py` | New | Session ORM + Pydantic |
| `backend/app/models/message.py` | New | Message models |
| `backend/app/models/api_key.py` | New | API key models |
| `backend/app/models/credit_ledger.py` | New | Ledger models |
| `backend/app/models/document.py` | New | Document/chunk models |
| `backend/app/models/common.py` | New | Shared enums/types |
| `backend/alembic/versions/002_core_schema.py` | New | Core tables |
| `backend/alembic/versions/003_rls_policies.py` | New | RLS SQL |
| `backend/tests/unit/test_models.py` | New | Model tests |
| `backend/tests/integration/test_migrations.py` | New | Migration smoke |

## Files to Modify
| File | Change |
|------|--------|
| `backend/alembic/env.py` | Wire async URL from Settings |
| `backend/app/config.py` | Database URL settings |

## Security & Secrets
`api_keys.encrypted_key` never returned in API responses. Service role key
server-only. RLS policies documented in migration comments.

## Dependencies
None new if SQLAlchemy/asyncpg already in pyproject.toml.

## Test Cases
### Happy Path
- Migration up/down on test DB → tables exist

### Edge Cases
- Duplicate session_id in messages → FK enforced

### Should Not Happen
- Application code using `supabase` client for DDL bypassing Alembic

## Manual Test Flow
1. Run `make migrate`
2. Supabase SQL editor: `\dt` equivalent — all tables listed
3. `SELECT * FROM sessions LIMIT 1` — empty, no error

## Phase/Feature Exit Signal
`make migrate` succeeds; integration test passes against dev Supabase.

## Notes & Assumptions
- Implement F008 before F002/F004/F007
- pgvector dimension 1536 default (OpenAI ada-002); configurable later
