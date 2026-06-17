# Context Map

Use this file to choose the smallest useful context set for a task.

## Always Load
- Current task from `tasks/IN_PROGRESS.md` or user prompt
- Relevant spec from `specs/`
- `docs/CONTEXT.md`
- Latest file in `turns/`

## By Task Type

| Task Type | Add These Files |
|---|---|
| Spec creation | `docs/forge.md`, `specs/_template.spec.md`, `docs/FEATURES.md` |
| Task breakdown | Relevant spec, `tasks/_format.md`, `docs/GIT_WORKFLOW.md` |
| Backend API | Relevant spec, `docs/CONVENTIONS.md`, `docs/ARCHITECTURE.md`, touched `backend/app/api/` and service files |
| Backend service | Relevant spec, `docs/CONVENTIONS.md`, touched `backend/app/services/`, related models/db files |
| Database | Relevant spec, `docs/ARCHITECTURE.md`, `docs/SECURITY.md`, touched `backend/app/db/`, migrations |
| LangGraph/core | Relevant spec, `docs/STATE.md`, `docs/ARCHITECTURE.md`, touched `backend/app/core/` |
| Frontend | Relevant spec, `docs/CONVENTIONS.md`, touched `frontend/` files |
| Infra | Relevant spec, `docs/ENVIRONMENT.md`, `docs/GIT_WORKFLOW.md`, touched `infra/` files |
| Security | `docs/SECURITY.md`, relevant spec, touched auth/secrets/logging files |
| Validation | `docs/VALIDATION.md`, relevant spec, Pydantic models |
| Logging | `docs/LOGGING.md`, `docs/SECURITY.md`, touched logging setup |
| Phase planning | `docs/PHASE_GATES.md`, `docs/FEATURES.md`, `.forge/workflows/` |
| Decisions | `docs/DECISIONS_LOG.md`, relevant ADR in `docs/adr/` |
| Agent prompts | `.forge/prompts/`, `tasks/_format.md` |
| Observability | Relevant spec, `docs/SECURITY.md`, `docs/WORLD_SIGNALS.md`, touched telemetry files |
| Docs-only | Target docs, `docs/CONTEXT.md`, latest turn file |

## Do Not Load By Default
- Full `docs/forge.md` during implementation unless validating scope
- Full `docs/ARCHITECTURE.md` for small UI or docs-only edits
- Unrelated source trees
- Generated reports unless the task is about reports

## Context Budget Rule
If context grows too large, stop and write a file list:
- Required files
- Optional files
- Files deliberately skipped

Then continue only with required files.
