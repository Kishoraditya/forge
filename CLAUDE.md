# FORGE — Claude Code Context

## What Is This
Forge is a self-hosted, BYOK (Bring Your Own Key), multi-session AI agent workbench. It is a composable harness + LLM, globally deployable on free infrastructure, investor-demonstrable, and enterprise-architecture-ready. Single admin, multiple anonymous simultaneous users (session-isolated, credit-limited). No logins. No persistence between sessions. Built on Option B conversation graph architecture from day one.

## Current Phase & Active Work
Phase: 0 — Core Engine (not yet started)
Active tasks: see tasks/IN_PROGRESS.md
Last updated: 2026-06-12

## Architecture in 10 Lines
```
FRONTEND        Next.js 14 + Tailwind + shadcn/ui + Zustand
API GATEWAY     FastAPI + Cloudflare Tunnel + CORS
AGENT CORE      LangGraph + DSPy + LiteLLM
TOOL LAYER      MCP + Custom Tools + Sandboxed Exec + WebSockets
CONTROL PLANE   Guardrails + Policy Engine + Human-in-Loop
ASYNC TASKS     Celery + Redis + Temporal
PERSISTENCE     Supabase (PostgreSQL + pgvector) + Neo4j/Memgraph
OBSERVABILITY   OpenTelemetry + Opik + PostHog + GrowthBook
INFRA           Docker + Terraform + Cloudflare + Railway
```

## Where Things Live
- API routes: backend/app/api/
- Agent core: backend/app/core/
- Tools & MCP: backend/app/tools/
- Pydantic models: backend/app/models/
- Database layer: backend/app/db/
- Graph (Neo4j): backend/app/graph/
- Services: backend/app/services/
- Specs: specs/phase-X/
- Tasks: tasks/
- Conventions: docs/CONVENTIONS.md
- Task format: tasks/_format.md
- Architecture: docs/ARCHITECTURE.md

## Rules (Non-Negotiable)
1. Read the spec file before writing any code
2. One function/file/module per task
3. All code has docstrings (see CONVENTIONS.md)
4. Write test first, then implementation
5. Update CONTEXT.md and IN_PROGRESS.md when task is done
6. Write `turns/Turn-XX-start.md` as first action and `turns/Turn-XX-stop.md` as last action in every response
7. Max 300 lines per file, max 50 lines per function
8. No business logic in API route handlers — delegate to services/
9. No direct database calls outside db/ layer
10. All async functions must be awaited (no fire-and-forget without Celery)

## Do Not
- Invent architecture not in ARCHITECTURE.md
- Create new dependencies without adding to pyproject.toml and noting in task
- Skip the spec file
- Write more than the task requires
- Create files not listed in the current task
- Touch files not listed in the current task
- Add hardcoded strings (use constants or config)

## Quick Commands
```
make dev        → start all local services
make test       → run full test suite
make lint       → run linting + type check
make spec F=F001 → scaffold spec for feature F001
make task       → scaffold new task
make context    → reminder to update CONTEXT.md
make flow F=F009 → show manual test flow for a feature
```

## Developer Signature (Required on Every File)
### Python:
```python
# =============================================================================
# forge / [module path]
# =============================================================================
# Description : [one sentence]
# Layer       : [Infra | API | Core | Tools | Memory | Observability]
# Feature     : [FXXX — Feature Name]
# Author      : [human | claude-code | cursor | codex] + KSR (reviewed by)
# Created     : YYYY-MM-DD
# Modified    : YYYY-MM-DD
# Version     : 0.1.0
# =============================================================================
```
### TypeScript/TSX:
```typescript
// =============================================================================
// forge / [module path]
// =============================================================================
// Description : [one sentence]
// Layer       : [Infra | API | Core | Tools | Memory | Observability]
// Feature     : [FXXX — Feature Name]
// Author      : [human | claude-code | cursor | codex] + KSR (reviewed by)
// Created     : YYYY-MM-DD
// Modified    : YYYY-MM-DD
// Version     : 0.1.0
// =============================================================================
```

## Spec-First Workflow
```
forge.md → spec file → human reviews → tasks → test first → implement → review → DONE.md
```
Never skip a step. The spec is the authority.

## turns/ — Crash Recovery
Write numbered turn files in `turns/` for every response:
- First action: create `turns/Turn-XX-start.md`
- Last action: create `turns/Turn-XX-stop.md`

Use the next available zero-padded turn number. If agent crashes, the latest
start/stop file tells the next session exactly where to resume.

## Context Loading Order
1. CLAUDE.md (~150 tokens)
2. CONTEXT.md (~400 tokens)
3. Current task (~200 tokens)
4. Relevant spec (~500 tokens)
5. Source files (as needed)

## The Lost Context Recovery Protocol
1. Read CLAUDE.md → understand the project
2. Read CONTEXT.md → understand current state
3. Read tasks/IN_PROGRESS.md → understand active work
4. Read docs/ARCHITECTURE.md → understand the system
5. Run `git log --oneline -20` → see recent history
6. Read the latest file in `turns/` → understand where the last session stopped
