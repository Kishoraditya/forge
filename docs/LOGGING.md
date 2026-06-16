# Logging Framework

Forge uses **structlog** for structured, JSON-friendly logs across the backend.

## Principles

1. Never log secrets, tokens, API keys, or raw BYOK credentials.
2. Include `correlation_id` on every request-scoped log (from middleware).
3. Include `session_id` when handling session-bound work (never in public logs).
4. Use event names in `snake_case` (e.g. `session_created`, `llm_call_failed`).
5. Redact fields listed in `docs/SECURITY.md` before emission.

## Standard Fields

| Field | When |
|-------|------|
| `event` | Always |
| `correlation_id` | Request-scoped |
| `session_id` | Session-scoped handlers |
| `feature_id` | Implementation tasks (e.g. `F004`) |
| `duration_ms` | External calls (LLM, DB, Redis) |
| `error_type` | On exceptions |

## Configuration

- `ENVIRONMENT=development`: console renderer, DEBUG level when `DEBUG=True`
- `ENVIRONMENT=production`: JSON renderer, INFO level
- Initialized in `backend/app/core/logging.py` (F001 task)

## Usage Pattern

```python
import structlog

logger = structlog.get_logger(__name__)

logger.info("session_created", session_id=session.id, budget_usd=budget)
```

## Error Logging

- Catch specific exceptions; log with `logger.exception` or `logger.error` + `error_type`.
- API layer maps exceptions to HTTP responses; do not return stack traces to clients.

## Tests

- Unit tests may use `structlog.testing.capture_logs()` to assert events.
- Integration tests must not assert on log file contents on disk.

## Related

- `docs/SECURITY.md` — redaction rules
- `docs/VALIDATION.md` — input validation vs logging
- `specs/phase-0/F001-scaffolding.spec.md` — logging bootstrap task
