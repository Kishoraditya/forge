# Turn-10 Start - 2026-06-17

## Branch
`feat/F003-f004-f005-conversation`

## Goal
Fix local dev: Redis connection fallback on ping failure; OpenRouter free models + env sync for LiteLLM.

## Spec
specs/phase-0/F003-llm-routing.spec.md, F004

## Files allowed
- backend/app/db/redis_client.py
- backend/app/config.py
- backend/app/constants.py
- backend/app/services/model_alias_service.py
- backend/app/core/llm_credentials.py
- backend/app/main.py
- backend/tests/unit/test_model_alias_service.py
- backend/tests/unit/test_redis_client.py
- .env.example
