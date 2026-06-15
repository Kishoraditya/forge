# FORGE - Workflow (Open This Every Session)

## Minimal Context Rule
Every agent turn loads only:
- `AGENTS.md`
- `docs/CONTEXT.md`
- `tasks/IN_PROGRESS.md`
- The latest file in `turns/`
- `docs/CONTEXT_MAP.md`

Load specs, task details, source files, and architecture docs only when the
current task requires them.

---

## turns/ - Crash-Recovery Files

Each agent response creates one start file and one stop file in `turns/`.

Naming:
- Start of response: `turns/Turn-XX-start.md`
- End of response: `turns/Turn-XX-stop.md`

Use the next available zero-padded turn number. Example:
- `turns/Turn-00-start.md`
- `turns/Turn-00-stop.md`
- `turns/Turn-01-start.md`
- `turns/Turn-01-stop.md`

Template:

```markdown
# Turn-XX Start|Stop - YYYY-MM-DD

## Status
[one line: what is happening right now]

## Task
[task ID + title from IN_PROGRESS.md, or planning/doc task]

## Done This Turn
- [bullet per completed action]

## Stopped At
[exact file, function, line, or document section - enough to resume cold]

## Next Action
[one sentence: what the next agent turn should do first]

## Uncommitted Files
[list changed files]

## Blockers
[anything needing human input]
```

Rule: the start file is the agent's first repo action; the stop file is the
agent's last repo action. If an agent crashes, resume from the newest file in
`turns/`.

---

## The Full Progression

### Stage 1 - Human Bootstrap Gate
Complete `tasks/HUMAN_TASKS.md` HT-001 through HT-008 before starting
AI-assisted Phase 0 work. This covers Git, scaffold review, `.env.local`, local
tooling, frontend initialization, local prerequisite checks, one Supabase dev
project, and one LLM provider key.

### Stage 2 - Create Phase 0 Specs (Agent)
Use Prompt A below.

### Stage 3 - Review Specs (Human, 1 spec at a time)
- Read each spec: are ACs binary testable? Is scope tight? Is data model right?
- Edit directly in the spec file if needed.
- Do not proceed to tasks until the spec is approved.

### Stage 4 - Populate Backlog (Agent)
Use Prompt B below.

### Stage 5 - Code a Task (Agent)
Use Prompt C below. One task per agent turn, max.
Work on the feature branch named in the task, never directly on `main`.

### Stage 6 - Review + Test (Human)
- Read the diff.
- Run `make test`.
- If passing: check task off in `DONE.md`, commit.
- If failing: use Prompt D below.

### Stage 7 - Update Docs
Update `docs/CONTEXT.md` and the current `turns/Turn-XX-stop.md`. Then repeat
from Stage 5.

### Stage 8 - Phase Complete Gate (Human)
- All tasks in `DONE.md` for phase?
- Run full test suite, save report to `reports/test/`.
- Run manual flows from `docs/MANUAL_TESTING.md`.
- `git tag phase-0-complete`
- Move to next phase, repeat from Stage 2.

---

## The 6 Prompts

### Prompt A - Create Specs for a Phase
```text
Read docs/forge.md and docs/CONTEXT.md.
Read specs/_template.spec.md.
Read docs/FEATURES.md.
Read the latest file in turns/.

Create spec files for Phase 0 features F001 through F008.
Location: specs/phase-0/FXXX-name.spec.md

Rules:
- One file per feature
- ACs must be binary (pass/fail, not subjective)
- Scope out anything not in forge.md
- Do not write any code
- Write turns/Turn-XX-start.md before and turns/Turn-XX-stop.md after

Show me F001 spec first. Wait for my approval before F002.
```

### Prompt B - Break Spec Into Tasks
```text
Read specs/phase-0/FXXX-name.spec.md and tasks/_format.md.
Read docs/GIT_WORKFLOW.md.
Read the latest file in turns/.

Break this feature into atomic tasks. Add to tasks/BACKLOG.md.

Rules:
- One task = one file or one function only
- Order by dependency
- Mark human vs agent
- Group tasks for the same feature on the same feature branch
- Include Files allowed and Files forbidden
- No code
- Write turns/Turn-XX-start.md before and turns/Turn-XX-stop.md after
```

### Prompt C - Implement One Task
```text
Read AGENTS.md, docs/CONVENTIONS.md, docs/CONTEXT_MAP.md, docs/WORLD_SIGNALS.md, and the latest file in turns/.
Read [spec file path].

Your task: [paste full task block from IN_PROGRESS.md]

Rules:
- Confirm branch from the task; do not work directly on main
- Before edits, state: spec read, task ID, files allowed, files forbidden, test plan
- Write test stubs first, then implementation
- Touch only the files listed in the task
- Follow CONVENTIONS.md exactly (header, docstring, naming)
- Follow SECURITY.md for secrets and telemetry-sensitive work
- Follow QUALITY_GATES.md before review
- When done: move task to DONE.md, update CONTEXT.md, write turns/Turn-XX-stop.md
- Tell me which tests pass before finishing
```

### Prompt D - Fix Failing Tests
```text
Read the latest file in turns/ and the failing test output below.

[paste test output]

Fix only what is failing. Do not refactor anything else.
Write turns/Turn-XX-stop.md when done.
```

### Prompt E - Resume After Crash
```text
Read AGENTS.md, docs/CONTEXT.md, and the latest file in turns/.

Continue from where the previous session stopped.
The latest turn file has the exact stopping point.
Confirm what you will do next before doing it.
```

### Prompt F - End of Session Cleanup
```text
Read the latest file in turns/ and tasks/IN_PROGRESS.md.

1. Update docs/CONTEXT.md with current project state
2. Write turns/Turn-XX-stop.md with final status and next action
3. List any uncommitted files
4. List anything that needs human action

Do not write any new code.
```

---

## Repeat Reminders

- Write `turns/Turn-XX-start.md` as your first repo action.
- Write `turns/Turn-XX-stop.md` as your last repo action.
- One file or function only.
- Write test first.
- Do not touch files not listed in the task.
- Show output before saving if unsure.

---

## If Agent Is Killed Mid-Task

1. Open the latest file in `turns/` and read "Stopped At" and "Uncommitted Files".
2. Check `git status`.
3. If partial code exists: either commit as WIP or revert only with explicit approval.
4. Move task back to `IN_PROGRESS.md` if it was prematurely moved.
5. Start new session with Prompt E.

---

## Doc Update Rules

| When | What to Update |
|---|---|
| Task completed | `DONE.md` + `CONTEXT.md` + `turns/Turn-XX-stop.md` |
| Task started | `IN_PROGRESS.md` + `turns/Turn-XX-start.md` |
| Agent turn starts | `turns/Turn-XX-start.md` |
| Agent turn ends | `turns/Turn-XX-stop.md` |
| Blocker found | `BLOCKED.md` + `turns/Turn-XX-stop.md` |
| Idea surfaces | `PARKING_LOT.md` |
| Phase done | `CONTEXT.md` + `CHANGELOG.md` + tag |
| Manual step done | `ENVIRONMENT.md` |

---

## Weekly Sanity Check

- Is `CONTEXT.md` accurate?
- Is `IN_PROGRESS.md` under 3 tasks?
- Is the latest file in `turns/` still relevant?
- Any items in `PARKING_LOT.md` ready to schedule?
- Does `make test` still pass?
