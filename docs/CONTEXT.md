# Project Context — 2026-06-17

## Status
F003–F005 verified complete (PR #3). F006 admin auth in progress on `feat/F006-admin-auth`.

## F001–F005 Verification (2026-06-17)
| Feature | Status | Notes |
|---------|--------|-------|
| F001 | Partial | P0-F001-001–007 done; Docker (008) + Alembic (009) pending |
| F003 | Done | Router, inference API, 41 tests, CI green |
| F004 | Done | Sessions, budget, Redis fallback, frontend store |
| F005 | Done | Messages API, SSE chat UI, all spec files present |
| CI | Pass | backend + frontend + ci-contract on PR #3 |

## What Was Just Done
- F006 P0-F006-001–005: `require_admin`, `/api/admin/me`, Supabase clients, login, middleware

## Next 3 Tasks
1. Merge PR #3 (F003–F005) then rebase F006
2. F006 RLS policies (blocked on F008-006)
3. P0-F001-008 Docker Compose dev stack
