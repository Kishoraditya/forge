# Turn-11 Start - 2026-06-17

## Branch
`feat/F003-f004-f005-conversation`

## Goal
Fix stale localStorage session 404 after backend restart; open PR.

## Files allowed
- frontend/hooks/use-session.ts
- frontend/lib/api/chat-client.ts
- backend/app/models/session.py
- backend/app/services/session_service.py
- backend/tests/integration/test_sessions_api.py
