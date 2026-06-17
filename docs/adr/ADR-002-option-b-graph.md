# ADR-002 — Option B Conversation Graph Architecture

**Status**: Accepted
**Date**: 2026-06-12
**Author**: human + KSR
**Reviewed by**: KSR

## Context

Forge must support branching, revisiting, and visualizing conversations as a
graph—not a flat message list.

## Decision

Adopt **Option B**: every message, tool call, and decision is a graph node;
relationships are first-class edges in Neo4j. Supabase holds relational/session
data; Neo4j holds conversation topology.

## Alternatives Considered

| Option | Pros | Cons |
|--------|------|------|
| Option A (flat messages) | Simpler | No native branching UX |
| Option B (full graph) | Matches investor demo vision | Dual persistence complexity |
| Option C (JSON blob graph) | No Neo4j early | Poor query/visualization |

## Consequences

### Positive
- React Flow UI (F032) maps directly to stored graph
- Audit trail via graph traversal

### Negative
- Must keep Supabase and Neo4j in sync for references

### Neutral
- Phase 0 uses Supabase messages only; graph writes begin Phase 1 (F009)

## Related

- **Spec**: F009, F031
- **Affects**: `backend/app/graph/`, `backend/app/core/`
- **Related ADRs**: ADR-006
