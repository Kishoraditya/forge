# ADR-001 — LangGraph Over AutoGen for Agent Orchestration

**Status**: Accepted
**Date**: 2026-06-12
**Author**: human + KSR
**Reviewed by**: KSR

## Context

Forge requires stateful, cyclic agent workflows with explicit graph persistence
(Option B conversation graph). Multiple orchestration frameworks were candidates.

## Decision

Use **LangGraph** as the sole agent orchestration engine. Do not use LangChain
agents or Microsoft AutoGen for production flows.

## Alternatives Considered

| Option | Pros | Cons |
|--------|------|------|
| LangGraph | Stateful graphs, interrupts, LangChain tool interop | Learning curve |
| AutoGen | Multi-agent conversations | Less explicit graph model for Option B |
| LangChain agents | Familiar API | Opaque loops, harder to audit |

## Consequences

### Positive
- Explicit nodes map to Neo4j edges in Phase 1+
- Human-in-the-loop via graph interrupts (F011)

### Negative
- Team must learn LangGraph patterns

### Neutral
- LangChain retained for tools/chains only, not agent loops

## Related

- **Spec**: F009 (Phase 1)
- **Affects**: `backend/app/core/`
- **Related ADRs**: ADR-002
