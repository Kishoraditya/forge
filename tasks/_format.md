# Task Format Guide

## What Is a Task
A task is the smallest deployable unit of work. One task equals one atomic
change: one function, one file, one database migration, one component, or one
config change. If it is larger, split it.

## Task ID Convention
`[PHASE]-[FEATURE]-[SEQUENCE]`

Examples:
- `P0-F001-001`
- `P1-F009-003`

## Mandatory Task Template

```markdown
---
### [TASK_ID] - [Short Title]

**Feature**: FXXX - [Feature Name]
**Spec**: specs/phase-X/FXXX-name.spec.md
**Branch**: feat/FXXX-short-name
**Assigned to**: [human / claude-code / cursor / codex]
**Status**: [backlog / in-progress / in-review / done / blocked]
**Estimated**: [S = <30min | M = 30-90min | L = split before work]
**Estimated tokens**: [low / medium / high]
**Actual**: [fill when done]
**Depends on**: [task_ids | none]

**Goal**:
[One sentence describing the outcome.]

**Files allowed**:
- `path/to/file.py`
- `path/to/test_file.py`

**Files forbidden**:
- Everything else unless the human updates this task first.

**Context required**:
- Read: `specs/phase-X/FXXX-name.spec.md`
- Read: `docs/CONVENTIONS.md`
- Read: [only the relevant source files]

**Implementation acknowledgment required before edits**:
- [ ] Spec file read
- [ ] Task ID stated
- [ ] Files allowed stated
- [ ] Files forbidden stated
- [ ] Test plan stated

**What to do**:
[Exact atomic change.]

**Tests required**:
- [ ] [Specific test command or test file]

**Acceptance criteria**:
- [ ] [Binary, testable condition]
- [ ] [Binary, testable condition]

**Dependency review**:
- [ ] No new dependency added
- [ ] If dependency added: justification, alternatives, security/license, size impact, and package files updated

**Definition of done**:
- [ ] Code implemented
- [ ] Unit tests pass
- [ ] Integration tests pass, if applicable
- [ ] Lint passes for touched area
- [ ] Types pass for touched area
- [ ] Spec requirement satisfied
- [ ] `docs/CONTEXT.md` updated
- [ ] `tasks/IN_PROGRESS.md` updated
- [ ] `turns/Turn-XX-stop.md` written
- [ ] Human review completed

**Do not**:
- Refactor unrelated code
- Touch files outside "Files allowed"
- Add unlisted behavior

**Handoff note**:
[If switching agents mid-task: stopped at file/function/line, next step, failing test.]

---
```

## Rules For Tasks
1. `IN_PROGRESS.md` has maximum 3 active tasks.
2. A task is not done until every Definition of Done item is checked.
3. Blocked tasks must include the blocker and the required human action.
4. Human tasks go in `HUMAN_TASKS.md`, not the main task lists.
5. Add unscheduled ideas to `PARKING_LOT.md`.
6. Always include dependencies to prevent ordering mistakes.
7. Always include allowed and forbidden files.
8. Group tasks for the same feature on the same feature branch.

## Task Sizing Guide

| Size | Time | Example |
|---|---:|---|
| S | <30 min | Add a model field plus one unit test |
| M | 30-90 min | Write one service function plus its test |
| L | 90 min+ | Split before work starts |

## Assignment Decision

| Task Type | Assign To |
|---|---|
| Boilerplate/scaffolding | Agent |
| Function from spec | Agent |
| Unit/integration tests | Agent |
| Env files and secrets | Human |
| Service accounts/API keys | Human |
| Review and approval | Human |
| Manual test flows | Human |
| Architectural decisions | Human decides, agent drafts |
| Database migration SQL | Agent drafts, human reviews |
| ADR writing | Human decides, agent drafts |
