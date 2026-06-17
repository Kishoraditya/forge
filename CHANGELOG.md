# Changelog

All notable changes to the Forge project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## When to update

| Event | Update CHANGELOG? | Section |
|-------|-----------------|---------|
| Each task/turn commit | Optional — use `[Unreleased]` for notable items | `[Unreleased]` |
| Feature branch merge to `main` | Yes, if user-facing or architectural | `[Unreleased]` |
| **Phase complete** (gate passed) | **Required** — cut version, move `[Unreleased]` → `[0.x.0]` | New version header + git tag |
| Hotfix release | Required | Patch version |

Per `docs/RITUALS.md` per-phase ritual: summarize phase work in CHANGELOG at phase
completion using Conventional Commits from that phase. Day-to-day task work does not
require a CHANGELOG line unless it is investor- or user-visible.

## [Unreleased]

### Added
- Phase 0 specs F001–F008 and atomic backlog (`specs/phase-0/`, `tasks/BACKLOG.md`)
- Governance: decision log, logging/validation frameworks, branch-only git flow, `.forge/` prompts
- F001 P0-F001-001: Pydantic Settings module (`backend/app/config.py`)
- F001 P0-F001-002: Application exception hierarchy (`backend/app/core/exceptions.py`)
- F001 P0-F001-003–007: FastAPI app factory, structlog, correlation middleware, health endpoint
- F003: LiteLLM inference router, rate limits, chat + streaming API
- F004: Anonymous sessions, budget tracking, Redis/in-memory fallback, session store (frontend)
- F005: Message CRUD, SSE streaming, chat UI with markdown rendering
- CI workflow (Python 3.12 backend, Node 24 frontend)

### Fixed
- Frontend `package-lock.json` synced for `npm ci` on CI (Node 24 / npm 11)
- Pin `@emnapi/core` and `@emnapi/runtime` at 1.11.1 for Linux `npm ci` parity
- CI contract tests (`backend/tests/ci/`) and `make ci-check` local parity target
- Mypy: enable `pydantic.mypy` plugin; fix `Settings()` strict `call-arg` on Linux CI
- Redis: ping-based fallback to in-memory when broker is unreachable
- OpenRouter dev path: env key sync, free model aliases, zero-cost for unmapped models
- LiteLLM debug noise suppressed; Next.js `turbopack.root` set for monorepo frontend

## [0.0.0] — 2026-06-12

### Added
- Project scaffold: folder structure, governance documents, templates
- CLAUDE.md — AI agent cold-start context file
- AGENTS.md — Multi-agent context file
- docs/ARCHITECTURE.md — System design document
- docs/CONVENTIONS.md — Coding standards and conventions
- docs/CONTEXT.md — Living project state document
- docs/ENVIRONMENT.md — Environment setup and API key reference
- docs/SCOPE.md — Future scope beyond current phases
- docs/RITUALS.md — Development ceremonies
- Spec template (specs/_template.spec.md)
- Task format guide (tasks/_format.md)
- Task board files (BACKLOG, IN_PROGRESS, DONE, BLOCKED, PARKING_LOT, HUMAN_TASKS, THIS_WEEK)
- ADR template (docs/adr/ADR-000-template.md)
- Makefile with developer commands
- Helper scripts (bootstrap.sh, create_spec.sh, create_task.sh, context_refresh.sh)
- pyproject.toml with full dependency list
- Pre-commit configuration (.pre-commit-config.yaml)
- GitHub PR template
- .gitignore
- .cursorrules for Cursor IDE

### Notes
- No product code written yet — this is the governance and scaffolding layer only
- Phase 0 specs and tasks are the next step
- See tasks/HUMAN_TASKS.md for Day 0 manual setup items
