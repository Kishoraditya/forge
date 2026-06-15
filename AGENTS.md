# FORGE — Agent Context (Codex / Agentic Assistants)

## What Is This
This file is for OpenAI Codex, Gemini, and other AI coding assistants working on the Forge project. Forge is a self-hosted, BYOK (Bring Your Own Key), multi-session AI agent workbench — a composable harness + LLM, globally deployable on free infrastructure, investor-demonstrable, and enterprise-architecture-ready. It supports a single admin with multiple anonymous simultaneous users (session-isolated, credit-limited). No logins. No persistence between sessions. Built on Option B conversation graph architecture.

If you are an AI coding agent: read this file in full before making any changes. Then read the relevant spec file and task description before writing code.

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

## Project Layout
```
forge/
├── backend/
│   └── app/
│       ├── api/           # FastAPI route handlers (thin — no business logic)
│       ├── core/          # LangGraph agent flows, DSPy modules
│       ├── services/      # Business logic layer
│       ├── models/        # Pydantic schemas and domain models
│       ├── db/            # Database access layer (Supabase, pgvector)
│       ├── graph/         # Neo4j graph operations
│       └── tools/         # MCP tool definitions, sandboxed execution
├── frontend/              # Next.js 14 application
├── infra/                 # Docker, Terraform, Cloudflare config
├── specs/                 # Feature specifications (phase-X/)
├── tasks/                 # Task tracking (IN_PROGRESS.md, DONE.md)
└── docs/                  # ARCHITECTURE.md, CONVENTIONS.md, CONTEXT.md
```

## Rules (Non-Negotiable)
1. Read the spec file before writing any code
2. One function/file/module per task
3. All code has docstrings (see docs/CONVENTIONS.md for format)
4. Write test first, then implementation
5. Update docs/CONTEXT.md and tasks/IN_PROGRESS.md when a task is done
6. Write `turns/Turn-XX-start.md` as first action and `turns/Turn-XX-stop.md` as last action in every response
7. Max 300 lines per file, max 50 lines per function
8. No business logic in API route handlers — delegate to services/
9. No direct database calls outside db/ layer
10. All async functions must be awaited (no fire-and-forget without Celery)

## Do Not
- Invent architecture not documented in docs/ARCHITECTURE.md
- Create new dependencies without adding to pyproject.toml and noting in the task
- Skip the spec file — the spec is the single source of truth
- Write more than the task requires
- Create files not listed in the current task
- Touch files not listed in the current task
- Add hardcoded strings — use constants or config

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

## turns/ — Crash Recovery
Write numbered turn files in `turns/` for every response:
- First action: create `turns/Turn-XX-start.md`
- Last action: create `turns/Turn-XX-stop.md`

Use the next available zero-padded turn number. If the agent session crashes,
the latest start/stop file tells the next session exactly where to resume.

## Context Loading Order
1. AGENTS.md (this file — ~150 tokens)
2. docs/CONTEXT.md (~400 tokens)
3. Current task from tasks/IN_PROGRESS.md (~200 tokens)
4. Relevant spec from specs/ (~500 tokens)
5. Source files (as needed)

## The Lost Context Recovery Protocol
If you have lost context or are starting a new session:
1. Read AGENTS.md → understand the project
2. Read docs/CONTEXT.md → understand current state
3. Read tasks/IN_PROGRESS.md → understand active work
4. Read docs/ARCHITECTURE.md → understand the system
5. Run `git log --oneline -20` → see recent history
6. Read the latest file in `turns/` → understand where the last session stopped

## Important Notes for Codex / Agentic Assistants
- This is a monorepo: backend/, frontend/, infra/ in a single repository
- Python 3.11+ with Poetry for dependency management
- FastAPI for the backend, Next.js 14 for the frontend
- LangGraph is the agent orchestration framework — not LangChain agents
- LiteLLM is the LLM abstraction layer — never call provider APIs directly
- Supabase is the primary relational database (PostgreSQL + pgvector)
- Neo4j is the conversation graph database (Option B architecture)
- All environment variables are documented in docs/ENVIRONMENT.md
- Test files live in backend/tests/ mirroring the app/ structure
