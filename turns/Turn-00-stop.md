# Turn-00 Stop - 2026-06-15

## Status
Bootstrap workflow and turn-file convention updated.

## Task
Make HT-001 through HT-008 the human-first bootstrap gate, move crash recovery
from root `TURN.md` to numbered files in `turns/`, and audit scaffold gaps.

## Done This Turn
- Created `turns/Turn-00-start.md`
- Reworked `tasks/HUMAN_TASKS.md` so HT-001 through HT-008 must be completed before AI-assisted Phase 0 work
- Moved local dev stack verification to deferred HT-009, after Docker Compose exists
- Updated `AGENTS.md`, `CLAUDE.md`, `docs/workflow.md`, `docs/RITUALS.md`, and `tasks/_format.md` to use `turns/Turn-XX-start.md` and `turns/Turn-XX-stop.md`
- Deleted retired root `TURN.md`
- Added `turns/README.md`
- Updated `docs/CONTEXT.md`, `docs/ENVIRONMENT.md`, `tasks/THIS_WEEK.md`, `.gitignore`, and `README.md` to match the new bootstrap flow
- Added context-engineering improvement ideas to `tasks/PARKING_LOT.md`

## Stopped At
Documentation-only workflow update complete.

## Next Action
Human should complete HT-001 through HT-008, then ask an agent to create Phase 0 specs using Prompt A in `docs/workflow.md`.

## Uncommitted Files
- `.gitignore`
- `AGENTS.md`
- `CLAUDE.md`
- `README.md`
- `docs/CONTEXT.md`
- `docs/ENVIRONMENT.md`
- `docs/RITUALS.md`
- `docs/workflow.md`
- `tasks/HUMAN_TASKS.md`
- `tasks/PARKING_LOT.md`
- `tasks/THIS_WEEK.md`
- `tasks/_format.md`
- `turns/README.md`
- `turns/Turn-00-start.md`
- `turns/Turn-00-stop.md`
- Deleted: `TURN.md`

## Blockers
Git repository is not initialized yet; complete HT-001 first.
