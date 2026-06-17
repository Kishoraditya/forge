# ADR-003 — LiteLLM for All LLM Provider Access

**Status**: Accepted
**Date**: 2026-06-12
**Author**: human + KSR
**Reviewed by**: KSR

## Context

Forge is BYOK: admins configure multiple providers. Direct SDK usage would
duplicate retry, streaming, cost, and fallback logic per provider.

## Decision

Route **all** LLM and embedding inference through **LiteLLM**. Application code
must not call Anthropic, OpenAI, or other provider SDKs directly.

## Alternatives Considered

| Option | Pros | Cons |
|--------|------|------|
| LiteLLM | Unified API, 100+ providers, cost tracking | Extra dependency |
| Native SDKs per provider | Full provider features | N× integration surface |
| Custom router | Minimal deps | Reinventing LiteLLM |

## Consequences

### Positive
- F002/F003 implement once against LiteLLM
- Model alias system maps cleanly to LiteLLM config

### Negative
- LiteLLM version upgrades need regression tests

### Neutral
- LangChain provider packages may wrap LiteLLM where convenient

## Related

- **Spec**: F002, F003
- **Affects**: `backend/app/core/`, `backend/app/services/`
- **Related ADRs**: ADR-001
