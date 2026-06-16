# F003 — LLM Routing & Inference Core
<!-- Spec version: 1.0.0 | Author: cursor | Date: 2026-06-17 -->

## Feature Reference
- **Feature ID**: F003
- **Phase**: Phase 0
- **Depends on**: F002
- **Blocks**: F004, F005, F007
- **Feature registry entry**: docs/FEATURES.md
- **Estimated tasks**: 8

## What This Does (One Paragraph)
Provides the internal LLM inference layer via LiteLLM: chat completion with
streaming (SSE), retries with exponential backoff, configurable fallback chain
across model aliases, per-provider rate limit counters in Redis, and per-call
token/cost accounting returned to callers.

## What This Does NOT Do
- Session budget enforcement (F004)
- LangGraph orchestration (Phase 1)
- Prompt optimization (DSPy — Phase 1)
- Direct provider SDK calls (forbidden per ADR-003)

## Acceptance Criteria
- [ ] AC1: `LLMRouterService.complete()` calls LiteLLM with alias-resolved model
- [ ] AC2: `LLMRouterService.stream()` yields SSE-compatible chunks
- [ ] AC3: Retry up to 3 times with backoff on transient errors
- [ ] AC4: Fallback chain: primary alias → secondary → tertiary on failure
- [ ] AC5: Redis tracks per-provider request counts for rate limiting hooks
- [ ] AC6: Response includes `prompt_tokens`, `completion_tokens`, `cost_usd`
- [ ] AC7: `POST /api/inference/chat` and `POST /api/inference/chat/stream` work
- [ ] AC8: Unit tests mock LiteLLM; one optional live smoke test gated by env flag

## Data Model
**InferenceRequest**: `messages: list[ChatMessage]`, `model_alias: str`,
`session_id: UUID | None`, `stream: bool`

**InferenceResult**: `content: str`, `prompt_tokens: int`, `completion_tokens: int`,
`cost_usd: float`, `model_used: str`

**ChatMessage**: `role: literal["system","user","assistant"]`, `content: str`

## Agent State Impact
Updates token counts via caller; does not persist messages (F004/F005).

## API Contract
`POST /api/inference/chat`
- Body: `InferenceRequest` (stream=false)
- Response 200: `InferenceResult`

`POST /api/inference/chat/stream`
- Body: `InferenceRequest` (stream=true)
- Response: `text/event-stream` SSE chunks `{ "delta": "..." }`, final event with usage

## Files to Create
| File | Type | Purpose |
|------|------|---------|
| `backend/app/core/llm_router.py` | New | LiteLLM wrapper |
| `backend/app/services/inference_service.py` | New | Business logic |
| `backend/app/services/rate_limit_service.py` | New | Redis counters |
| `backend/app/api/inference.py` | New | HTTP routes |
| `backend/app/models/inference.py` | New | Pydantic schemas |
| `backend/tests/unit/test_llm_router.py` | New | Router tests |
| `backend/tests/unit/test_inference_service.py` | New | Service tests |
| `backend/tests/integration/test_inference_api.py` | New | API tests |

## Files to Modify
| File | Change |
|------|--------|
| `backend/app/main.py` | Register inference router |
| `backend/app/constants.py` | Retry/fallback constants |

## Security & Secrets
LiteLLM receives keys from BYOK service only. No keys in request bodies.

## Dependencies
None new (litellm, redis already declared).

## Test Cases
### Happy Path
- Mock LiteLLM success → correct token/cost fields

### Edge Cases
- Primary fails, fallback succeeds
- Rate limit counter increments

### Should Not Happen
- Import of `anthropic` or `openai` SDK in router

## Manual Test Flow
1. Configure alias `fast` in admin BYOK
2. `curl -X POST /api/inference/chat` with test message
3. Response text and token counts returned

## Phase/Feature Exit Signal
Live provider smoke test passes with `RUN_LIVE_LLM_TESTS=1`.

## Notes & Assumptions
- Cost calculation uses LiteLLM built-in cost map
- Streaming protocol matches frontend SSE client in F005
