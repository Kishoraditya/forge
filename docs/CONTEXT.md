# Project Context — 2026-06-17

## Status
F003–F005 complete on `feat/F003-f004-f005-conversation`. F001 scaffold items
P0-F001-003 through P0-F001-007 landed alongside the conversation stack.

## What Was Just Done
- Backend: LiteLLM router, inference/sessions/messages APIs, in-memory persistence
- Frontend: Zustand session store, SSE chat client, full chat UI
- 36 backend tests passing; frontend lint + build pass

## Next 3 Tasks
1. P0-F001-008 — Docker Compose dev stack
2. P0-F001-009 — Alembic bootstrap
3. P0-F008-001 — Supabase schema (replace in-memory store)
