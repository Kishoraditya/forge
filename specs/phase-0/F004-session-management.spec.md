# F004 — Session Management
<!-- Spec version: 1.0.0 | Author: cursor | Date: 2026-06-17 -->

## Feature Reference
- **Feature ID**: F004
- **Phase**: Phase 0
- **Depends on**: F003, F008
- **Blocks**: F005
- **Feature registry entry**: docs/FEATURES.md
- **Estimated tasks**: 9

## What This Does (One Paragraph)
Creates anonymous sessions on first visit (UUID, no login), stores session
metadata in Supabase, caches active state in Redis, enforces per-session credit
budget with hard stop, supports configurable TTL (default 2h inactivity), and
exposes budget/token data to the frontend in real time.

## What This Does NOT Do
- User accounts or login
- Cross-session memory
- Payment processing
- Admin session impersonation

## Acceptance Criteria
- [ ] AC1: `POST /api/sessions` creates session with default budget from config
- [ ] AC2: Session persisted in `sessions` table with `budget_remaining_usd`
- [ ] AC3: Redis mirrors session state for fast budget checks
- [ ] AC4: Each inference call decrements budget via `credit_ledger` entry
- [ ] AC5: Budget exhausted → `BudgetExceededError` (402) with user-safe message
- [ ] AC6: TTL expiry marks session `expired`; new inference rejected
- [ ] AC7: `GET /api/sessions/{id}` returns token count and budget remaining
- [ ] AC8: Frontend Zustand store holds `sessionId` and budget display fields

## Data Model
**SessionCreateResponse**: `id: UUID`, `budget_remaining_usd: float`, `expires_at: datetime`

**SessionStatus**: `id`, `status`, `token_count`, `budget_remaining_usd`, `model_alias`

## Agent State Impact
`session_id`, `budget_remaining_usd`, `model_alias` — owner: session service.

## API Contract
`POST /api/sessions` → 201 `SessionCreateResponse`
`GET /api/sessions/{session_id}` → 200 `SessionStatus`
`PATCH /api/sessions/{session_id}/touch` → extends activity TTL

## Files to Create
| File | Type | Purpose |
|------|------|---------|
| `backend/app/services/session_service.py` | New | Create/update/expiry |
| `backend/app/services/budget_service.py` | New | Ledger + enforcement |
| `backend/app/db/session_repository.py` | New | Supabase persistence |
| `backend/app/db/redis_client.py` | New | Redis session cache |
| `backend/app/api/sessions.py` | New | Session routes |
| `backend/tests/unit/test_session_service.py` | New | Unit tests |
| `backend/tests/unit/test_budget_service.py` | New | Budget tests |
| `backend/tests/integration/test_sessions_api.py` | New | API tests |
| `frontend/lib/stores/session-store.ts` | New | Zustand store |
| `frontend/hooks/use-session.ts` | New | Session bootstrap hook |

## Files to Modify
| File | Change |
|------|--------|
| `backend/app/main.py` | Register sessions router |
| `backend/app/services/inference_service.py` | Call budget_service after inference |
| `backend/app/config.py` | `DEFAULT_SESSION_BUDGET_USD`, `SESSION_TTL_SECONDS` |

## Security & Secrets
Session IDs are UUIDs; no PII. Rate limit session creation per IP (stub for F028).

## Dependencies
- `zustand` — frontend session state

## Test Cases
### Happy Path
- Create session → inference → budget decreases

### Edge Cases
- Budget exactly 0 → next call fails with 402
- Expired session → 404 or 410

### Should Not Happen
- Negative budget_remaining_usd

## Manual Test Flow
1. Open app → session created in network tab
2. Send chat until budget exhausted → banner shown

## Phase/Feature Exit Signal
Integration test proves budget hard stop; UI shows live token counter.

## Notes & Assumptions
- Default budget $0.10 USD configurable in admin later
- Session cookie or localStorage for session_id on frontend
