# F002 — BYOK Configuration System
<!-- Spec version: 1.0.0 | Author: cursor | Date: 2026-06-17 -->

## Feature Reference
- **Feature ID**: F002
- **Phase**: Phase 0
- **Depends on**: F001, F008
- **Blocks**: F003
- **Feature registry entry**: docs/FEATURES.md
- **Estimated tasks**: 9

## What This Does (One Paragraph)
Lets the admin configure BYOK provider API keys and model aliases (`fast`,
`smart`, `cheap`) via a protected admin UI and API. Keys are encrypted at rest
in Supabase, validated with a live LiteLLM health check before save, and used
to auto-generate LiteLLM routing configuration.

## What This Does NOT Do
- End-user key entry (admin only)
- Multiple admin accounts (F006 scope)
- Automatic key rotation
- Storing keys in `.env` for production paths

## Acceptance Criteria
- [ ] AC1: Admin can POST provider key; key encrypted in `api_keys` table
- [ ] AC2: Health check endpoint validates key with LiteLLM before persist
- [ ] AC3: Model alias CRUD: alias → provider + model name
- [ ] AC4: LiteLLM config generated from active aliases and keys
- [ ] AC5: API never returns decrypted keys in responses
- [ ] AC6: Admin UI page at `/admin/byok` lists providers and alias editor
- [ ] AC7: Unit tests mock LiteLLM; integration test uses test DB

## Data Model
**ModelAlias** (Pydantic): `alias: str`, `provider: str`, `model_name: str`,
`is_default: bool`

**ProviderKeyCreate**: `provider: str`, `api_key: str` (write-only)

**ProviderKeyResponse**: `provider`, `is_active`, `last_validated_at` (no key)

## Agent State Impact
`model_alias` field in agent state resolved via alias service.

## API Contract
`POST /api/admin/byok/keys` — body: `ProviderKeyCreate` → 201
`POST /api/admin/byok/keys/{provider}/validate` → `{ "valid": bool }`
`GET /api/admin/byok/aliases` → list `ModelAlias`
`PUT /api/admin/byok/aliases/{alias}` → update alias

All require admin auth (F006); stub dependency until F006 lands.

## Files to Create
| File | Type | Purpose |
|------|------|---------|
| `backend/app/services/byok_service.py` | New | Key validate/store |
| `backend/app/services/model_alias_service.py` | New | Alias CRUD |
| `backend/app/services/litellm_config_service.py` | New | Config generation |
| `backend/app/db/api_key_repository.py` | New | Encrypted persistence |
| `backend/app/api/admin_byok.py` | New | Admin routes |
| `backend/app/models/byok.py` | New | Pydantic schemas |
| `backend/tests/unit/test_byok_service.py` | New | Service tests |
| `backend/tests/unit/test_litellm_config_service.py` | New | Config tests |
| `frontend/app/admin/byok/page.tsx` | New | Admin UI |

## Files to Modify
| File | Change |
|------|--------|
| `backend/app/main.py` | Register admin_byok router |

## Security & Secrets
Encrypt with Fernet or Supabase Vault pattern; key material never logged.
Admin-only routes. See `docs/SECURITY.md`.

## Dependencies
- `cryptography` — Fernet encryption if not using Vault API directly
- Justification: standard symmetric encryption for at-rest keys

## Test Cases
### Happy Path
- Valid Anthropic key → validate true → stored encrypted

### Edge Cases
- Invalid key → validate false, not stored
- Duplicate provider → upsert behavior

### Should Not Happen
- GET endpoint returning plaintext key

## Manual Test Flow
1. Login as admin
2. Enter Anthropic key → Validate → Save
3. DB row exists; API GET shows provider without key

## Phase/Feature Exit Signal
Alias `fast` maps to configured model; LiteLLM config loads from DB.

## Notes & Assumptions
- Dev may fall back to `ANTHROPIC_API_KEY` in `.env.local` until admin saves DB key
- F006 auth dependency injected when available
