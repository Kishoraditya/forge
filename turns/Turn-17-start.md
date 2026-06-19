# Turn 17 — Start

## Goal
Finalize Phase 0 (F001 Docker/Alembic, F008 schema, F002 BYOK, F007 RAG remainder).

## Approach
- Alembic migrations + SQLAlchemy ORM for production Supabase
- In-memory fallback when DATABASE_URL unset (tests/dev without Postgres)
- Complete BYOK + RAG + admin UI
