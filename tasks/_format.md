# Task Format Guide

## What Is a Task
A task is the smallest deployable unit of work. One task = one atomic change.
It may be a single function, a single file, a single database migration,
a single component, or a single config change. Never more than one thing.

## Task ID Convention
[PHASE]-[FEATURE]-[SEQUENCE]
Example: P0-F001-001, P1-F009-003

## Task File Template (used in BACKLOG.md, IN_PROGRESS.md, DONE.md)

---
### [TASK_ID] — [Short Title]

**Spec**: specs/phase-X/FXXX-name.spec.md
**Assigned to**: [human / claude-code / cursor / codex]
**Status**: [backlog / in-progress / in-review / done / blocked]
**Estimated**: [S = <30min | M = 30-90min | L = 90min+]
**Actual**: [fill when done]
**Depends on**: [task_ids | none]

**What to do (one sentence)**:
Create `backend/app/services/session_service.py` with `create_session()` function.

**Acceptance checklist**:
- [ ] File created at correct path
- [ ] Function signature matches spec AC1
- [ ] Docstring present (see CONVENTIONS.md)
- [ ] Unit test written and passing
- [ ] No new imports added without updating pyproject.toml
- [ ] CONTEXT.md updated after completion
- [ ] `turns/Turn-XX-stop.md` updated

**Context needed**:
- Read: specs/phase-0/F004-session-management.spec.md
- Read: docs/CONVENTIONS.md (docstring format)
- Reference: backend/app/models/session.py (Pydantic schema)

**Do not**:
- Implement session expiry (that is P0-F004-003, a separate task)
- Modify database schema (that is P0-F004-001)

**Definition of done**:
`pytest tests/unit/test_session_service.py` passes.
Function is importable. Docstring present.

**Handoff note** (if switching agents mid-task):
Stopped at [function/line], next step is [X], test failing at [Y].

---

## Rules for Tasks
1. Tasks in IN_PROGRESS.md: maximum 3 at any time
2. A task is not "done" until all checklist items are checked
3. Blocked tasks must have a blocker description
4. Human tasks go in HUMAN_TASKS.md, not the main lists
5. Add to PARKING_LOT.md anything that comes up but isn't scheduled
6. Always include `Depends on` field to prevent ordering mistakes

## Task Sizing Guide
| Size | Time | Example |
|------|------|---------|
| S | <30min | Add a Pydantic model field, write one unit test, update one import |
| M | 30-90min | Write one service function + its test, create one API endpoint |
| L | 90min+ | Split this task. If you can't, it's a design problem. |

## Task Assignment Decision
| Task Type | Assign To |
|-----------|-----------|
| Write boilerplate/scaffolding | Agent (Claude Code) |
| Implement a function from spec | Agent |
| Write unit tests for a function | Agent |
| Write integration tests | Agent |
| Create env files, fill secrets | Human |
| Make service accounts (APIs) | Human |
| Review + approve agent output | Human |
| Manual test flows | Human |
| Architectural decisions | Human |
| Docker Compose initial setup | Human |
| Database migration SQL | Human reviews, agent drafts |
| ADR writing | Human decides, agent drafts |

## Definition of Done Checklist
- [ ] Code implemented
- [ ] Unit tests pass
- [ ] Integration tests pass (if applicable)
- [ ] Docs updated
- [ ] CONTEXT.md updated
- [ ] `turns/Turn-XX-stop.md` updated
- [ ] Manual test flow documented (if new feature)
- [ ] Acceptance criteria met
- [ ] Human approved
