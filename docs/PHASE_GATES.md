# Phase Gates

Definition of "shippable" per phase. A phase is complete only when every item
below passes.

## Phase 0 — Core Engine

| Gate | Requirement |
|------|-------------|
| Specs | F001–F008 specs approved; all ACs checked |
| Tasks | All P0-F00x tasks in DONE.md |
| Unit tests | `make test-unit` passes |
| Integration | `make test-integration` passes for session, LLM, health |
| Lint/types | `make lint` passes |
| Migrations | `make migrate` applies cleanly on fresh Supabase dev DB |
| Live LLM | One provider completes a round-trip via LiteLLM |
| Session | Anonymous session created; budget enforced at limit |
| UI | Chat sends message and renders streamed markdown response |
| Admin | Admin routes reject unauthenticated access |
| Manual | Phase 0 flows in `docs/MANUAL_TESTING.md` pass |
| Coverage | ≥70% on `backend/app/services/` and `backend/app/core/` |

## Phase 1 — Agent Intelligence Layer

| Gate | Requirement |
|------|-------------|
| Specs | F009–F020 approved and implemented |
| Graph | LangGraph StateGraph executes full node loop |
| Tools | At least one MCP tool and one custom tool callable |
| Sandbox | Code execution works (local Docker or e2b per ADR) |
| Manual | All Phase 1 MANUAL_TESTING flows pass |

## Phase 2 — Observability & Control Plane

| Gate | Requirement |
|------|-------------|
| Telemetry | OpenTelemetry traces visible locally |
| Guardrails | Policy engine blocks configured unsafe outputs |
| Cost | Dashboard shows per-session spend |

## Phase 3–5

See `docs/FEATURES.md` completion gates per feature. Phase retrospective ADR
required before tagging `phase-N-complete`.
