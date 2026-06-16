# F006 — Single Admin Authentication
<!-- Spec version: 1.0.0 | Author: cursor | Date: 2026-06-17 -->

## Feature Reference
- **Feature ID**: F006
- **Phase**: Phase 0
- **Depends on**: F001, F008
- **Blocks**: F002 (full enforcement), F007
- **Feature registry entry**: docs/FEATURES.md
- **Estimated tasks**: 8

## What This Does (One Paragraph)
Implements single-admin authentication via Supabase Auth: login page, JWT session
for admin, Next.js middleware protecting `/admin/*`, FastAPI dependency
verifying admin JWT on protected routes, and RLS policies ensuring only admin
can read/write configuration tables.

## What This Does NOT Do
- Multi-admin or RBAC
- Anonymous user login
- OAuth providers beyond email/password
- Password reset flows (manual Supabase dashboard)

## Acceptance Criteria
- [ ] AC1: Admin login at `/admin/login` with Supabase email/password
- [ ] AC2: Unauthenticated access to `/admin/*` redirects to login
- [ ] AC3: FastAPI `require_admin` dependency validates JWT on admin routes
- [ ] AC4: Public chat routes remain unauthenticated
- [ ] AC5: RLS: `api_keys`, `documents`, admin config tables admin-only
- [ ] AC6: Logout clears session
- [ ] AC7: Tests use mocked JWT validation

## Data Model
**AdminUser** (from Supabase JWT claims): `sub`, `email`, `role: "admin"`

## Agent State Impact
None.

## API Contract
Admin routes use `Authorization: Bearer <jwt>` header.
`GET /api/admin/me` → `{ "email": str, "role": "admin" }`

## Files to Create
| File | Type | Purpose |
|------|------|---------|
| `backend/app/core/auth.py` | New | JWT verification dependency |
| `backend/app/api/admin_auth.py` | New | Admin me endpoint |
| `backend/tests/unit/test_auth.py` | New | Auth tests |
| `frontend/app/admin/login/page.tsx` | New | Login UI |
| `frontend/app/admin/layout.tsx` | New | Admin layout |
| `frontend/middleware.ts` | New | Route protection |
| `frontend/lib/supabase/client.ts` | New | Supabase browser client |
| `frontend/lib/supabase/server.ts` | New | Server client |

## Files to Modify
| File | Change |
|------|--------|
| `backend/app/api/admin_byok.py` | Add `require_admin` |
| `backend/alembic/versions/003_rls_policies.py` | Admin RLS rules |
| `frontend/package.json` | Add `@supabase/supabase-js` |

## Security & Secrets
JWT secret from Supabase. Service role key never exposed to frontend.
See `docs/SECURITY.md`.

## Dependencies
- `@supabase/supabase-js` — auth client
- `@supabase/ssr` — Next.js SSR helpers

## Test Cases
### Happy Path
- Valid admin JWT → admin route 200

### Edge Cases
- Missing token → 401
- Expired token → 401

### Should Not Happen
- Anonymous user reading `api_keys` table via API

## Manual Test Flow
1. Visit `/admin/byok` unauthenticated → redirect login
2. Login with admin credentials → BYOK page loads

## Phase/Feature Exit Signal
All admin API routes reject without valid JWT.

## Notes & Assumptions
- Single admin user created manually in Supabase dashboard (human step in ENVIRONMENT.md)
- F002 can stub admin dependency until F006 merges; then wire fully
