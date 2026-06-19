# Turn 17 — Stop

## Completed on feat/F007-rag
- F001: Docker compose + Dockerfiles, Alembic 001–003
- F008: ORM models, pgvector schema, RLS migration, db session factory
- F002: BYOK encryption, api key repo, services, admin API + UI
- F007: embedding, document repo, RAG service, admin documents API + UI, chat RAG injection
- 55 backend tests pass; frontend lint + build pass

## Production notes
- Run `make migrate` with `DATABASE_URL` for Supabase tables
- Sessions/messages still use in-memory store until wired to Postgres repos (schema ready)
- `make dev` starts redis, neo4j, backend, frontend via Docker
