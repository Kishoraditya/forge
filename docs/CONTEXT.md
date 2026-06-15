# Project Context — 2026-06-12

## Status
Phase 0 not started. Project scaffold complete. No code written yet.

## What Was Just Done
- Project folder structure created
- Governance documents created (CLAUDE.md, CONVENTIONS.md, ARCHITECTURE.md)
- Spec and task templates created
- Makefile and helper scripts created
- pyproject.toml initialized with all dependencies
- Pre-commit hooks configured

## What Is In Progress
- Nothing — scaffold just completed

## What's Blocked
- Nothing

## Key Decisions Made
- Monorepo structure: backend/, frontend/, infra/ in single repo
- Python 3.11+ with Poetry for dependency management
- Spec-driven development workflow adopted
- Option B conversation graph architecture selected
- LangGraph for agent orchestration (not LangChain agents)
- LiteLLM as the LLM abstraction layer (all providers go through LiteLLM)
- Supabase for relational persistence + pgvector for embeddings
- Neo4j AuraDB for conversation graph storage
- Upstash Redis for caching and Celery broker
- FastAPI for the backend API layer
- Next.js 14 with App Router for the frontend

## Environment State
- Human bootstrap gate: HT-001 through HT-008 must be completed before AI-assisted Phase 0 spec/task work begins
- `.env.local`: present locally and ignored by Git; must contain placeholders plus Supabase dev credentials and one LLM provider key after HT-008
- Local Docker Compose: not yet configured; schedule after F001 local-dev task exists
- Supabase: one development project is required during bootstrap; production/staging projects deferred
- Neo4j AuraDB: deferred until hosted graph integration is required; local Docker Neo4j is enough before then
- Upstash Redis: deferred until hosted Redis/deployment parity is required; local Docker Redis is enough before then
- Observability keys: deferred until the matching Phase 2 observability feature is scheduled
- Turn recovery: root `TURN.md` is retired; use numbered files in `turns/`

## Next 3 Tasks
1. Human: Initialize Git repository
2. Human: Review and approve scaffold
3. Human: Complete HT-003 through HT-008, then ask AI to create Phase 0 specs
