# Validation Framework

Input and state validation rules for Forge. Specs reference this document;
implementation uses Pydantic v2 at boundaries.

## Layers

| Layer | Tool | Responsibility |
|-------|------|----------------|
| API | Pydantic request/response models | HTTP shape, types, bounds |
| Service | Pydantic + custom validators | Business rules |
| Config | `pydantic-settings` | Environment variables |
| State | Pydantic `AgentState` fields | LangGraph state contract (`docs/STATE.md`) |
| DB | SQLAlchemy + Alembic constraints | Persistence integrity |

## Rules

1. Validate at the outermost layer that receives untrusted input (API or WebSocket).
2. Services assume validated models; re-validate only when crossing trust boundaries.
3. Use `Field(..., ge=, le=, min_length=)` for numeric and string bounds.
4. Reject unknown fields on admin/config payloads (`model_config = ConfigDict(extra="forbid")`).
5. Return HTTP 422 with structured error body from FastAPI; never leak internal paths.
6. Budget and session IDs must be UUID v4 format where applicable.

## Standard Error Shape

```json
{
  "detail": [
    {"loc": ["body", "field"], "msg": "...", "type": "value_error"}
  ],
  "correlation_id": "uuid"
}
```

## Custom Exceptions

Use classes from `backend/app/core/exceptions.py` (F001):

| Exception | HTTP | When |
|-----------|------|------|
| `ValidationError` (app) | 422 | Business rule failure |
| `NotFoundError` | 404 | Missing session/resource |
| `BudgetExceededError` | 402 | Session budget exhausted |
| `UnauthorizedError` | 401 | Admin auth failure |
| `ForbiddenError` | 403 | RLS or policy denial |

## Testing

- Every validator gets a unit test with valid, invalid, and edge inputs.
- Property-based tests optional for complex parsers (Phase 5).

## Related

- `docs/CONVENTIONS.md` — docstrings and naming
- `docs/STATE.md` — agent state validation requirements per feature
