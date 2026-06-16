# FORGE - Agent Context

## Canonical Source
This file is the source of truth for OpenAI Codex, Claude Code, Gemini, Cursor,
and other AI coding assistants working on Forge. Assistant-specific files such
as `CLAUDE.md` must point here instead of duplicating rules.

Forge is a self-hosted, BYOK, multi-session AI agent workbench. User-facing
sessions are ephemeral: anonymous users do not get durable accounts or durable
personal session continuity. System telemetry, graph relationships, audit
records, platform configuration, and metrics may persist according to the
architecture.

## Current Phase
- Phase: 0 - Core Engine
- Status: in progress (F001 scaffolding)
- Human gate: HT-001 through HT-008 complete
- Python: `poetry env use python3.12` (required; 3.14 breaks dependencies)

## Architecture In 10 Lines
```text
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

## Minimum Context Loading Order
Load the smallest context that can safely complete the task:
1. Current task from `tasks/IN_PROGRESS.md` or the user-provided task
2. Relevant spec from `specs/`
3. `docs/CONTEXT.md`
4. Latest file in `turns/`
5. `docs/CONTEXT_MAP.md` for routing to any extra docs
6. Source files listed by the task

Read `docs/ARCHITECTURE.md` only for architecture-sensitive work. Read
`docs/forge.md` only for spec creation or scope validation.

## Turn Files
Every agent response must create numbered turn files:
- First repo action: `turns/Turn-XX-start.md`
- Last repo action: `turns/Turn-XX-stop.md`

Use the next available zero-padded turn number. If a session crashes, resume
from the newest file in `turns/`.

Turn stop files must record tests run or explicitly state when tests are not
required. Commit each completed turn on a feature branch — never directly on
`main` (see `docs/GIT_WORKFLOW.md`). Log material decisions in
`docs/DECISIONS_LOG.md`.

## Implementation Acknowledgment
Before any implementation edit, state these in the user-visible update or turn
file:
- Spec file read
- Task ID
- Files allowed to modify
- Files forbidden
- Test plan

Do not implement until these are known.

## Non-Negotiable Rules
1. Spec first: no implementation without reading the relevant spec.
2. One atomic task at a time: one function, file, module, migration, or config.
3. Tests first: write or update the failing test before implementation.
4. Allowed files only: touch only files listed in the task.
5. No opportunistic refactors: modify only lines required for the task.
6. No business logic in API routes: API calls services.
7. Database access originates in `backend/app/db/`; services call db.
8. Core graph code calls services, not database clients directly.
9. All async functions must be awaited; no fire-and-forget without Celery.
10. Max 300 lines per file and 50 lines per function.
11. All code has docstrings according to `docs/CONVENTIONS.md`.
12. No hardcoded strings where config/constants are appropriate.

## Branch Workflow
Never do feature work directly on `main`. Group tasks by feature and work on a
feature branch:
- Feature branch: `feat/FXXX-short-name`
- Fix branch: `fix/FXXX-short-desc`
- Docs branch: `docs/FXXX-short-desc` or `docs/scaffold-short-desc`

Before opening or merging a PR, sync with remote:
```bash
git fetch origin
git checkout main
git pull --ff-only origin main
git checkout feat/FXXX-short-name
git rebase main
```

If another simultaneous branch updates shared files, fetch and rebase before
continuing:
```bash
git fetch origin
git rebase origin/main
```

Resolve conflicts manually, rerun quality gates, then push with lease:
```bash
git push --force-with-lease
```

See `docs/GIT_WORKFLOW.md` for the full branch and merge process.

## Cost Control
Prefer the cheapest capable model for agent workflows:
1. Cheap model for formatting, simple edits, summaries, and routing
2. Fast model for ordinary coding tasks
3. Smart model only for architecture, debugging hard failures, or low-confidence work

Use live LLM calls only when the task requires live inference. Mock provider
calls in tests unless the task is explicitly a live integration test.

## Security Rules
- Never log API keys, service-role keys, tokens, cookies, or credentials.
- Never return secret values in final answers or test output summaries.
- Secrets only come from environment variables or approved secret stores.
- Provider credentials are never stored in plaintext.
- Redact sensitive values in telemetry, traces, logs, screenshots, and reports.
- Do not commit `.env.local` or generated credential files.
- Treat Supabase service-role keys as privileged server-only secrets.

See `docs/SECURITY.md` for detailed rules.

## Dependency Governance
New dependencies require:
- Justification in the task or PR
- Alternatives considered
- Security/licensing review
- Size/runtime impact note
- Update to `pyproject.toml`, package lock files, or frontend package files
- Quality gates rerun

Do not add dependencies for convenience if standard library or existing project
libraries are sufficient.

## Developer Signature
Every new Python/TypeScript file must include the project signature from
`docs/CONVENTIONS.md`.

## Important Project Notes
- Monorepo: `backend/`, `frontend/`, `infra/`
- Python 3.11+ with Poetry
- FastAPI backend, Next.js 14 frontend
- LangGraph for orchestration, not LangChain agents
- LiteLLM for all provider access; never call provider APIs directly
- Supabase for relational/vector persistence
- Neo4j for conversation graph persistence
- Environment variables are documented in `docs/ENVIRONMENT.md`
- Canonical feature list lives in `docs/FEATURES.md`
- Agent state contract lives in `docs/STATE.md`
- Dynamic context signals live in `docs/WORLD_SIGNALS.md`
