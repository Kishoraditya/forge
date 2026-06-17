# Development Rituals

These ceremonies are non-negotiable. They keep context alive and prevent drift.

## Session Start Ritual
1. Create the next `turns/Turn-XX-start.md`.
2. Open `docs/CONTEXT.md` and read it in full.
3. Open `tasks/IN_PROGRESS.md`.
4. Open the latest previous file in `turns/`.
5. Open `docs/CONTEXT_MAP.md` to choose only the extra files needed.
6. Capture world signals from `docs/WORLD_SIGNALS.md`: branch, task, feature, allowed files, required tests.
7. If continuing a task: re-read the spec file and task description.
8. If starting new: pick from `BACKLOG.md`, move to `IN_PROGRESS.md`.
9. Begin.

## Session End Ritual
1. Is the current task done?
   - Yes: move it to `DONE.md`, check all checklist items, note actual time.
   - No: note where you stopped in `IN_PROGRESS.md`.
2. Update `docs/CONTEXT.md`.
3. Create the matching `turns/Turn-XX-stop.md` including **Tests run** (command + result, or "not required" with reason).
4. Append decision rows to `docs/DECISIONS_LOG.md` when human or LLM made a material choice.
5. Run tests when code changed; record in turn stop file. Docs-only turns: state "Tests: not required (docs-only)."
6. **Commit the turn** on the active feature branch per `docs/GIT_WORKFLOW.md` — never on `main`.
7. Check `PARKING_LOT.md` for new ideas.

## Per-Task Ritual

### Before
- Read spec AC list.
- Read task "context needed" files.
- Confirm branch from the task and sync it using `docs/GIT_WORKFLOW.md`.
- State implementation acknowledgment: spec read, task ID, files allowed, files forbidden, test plan.
- Confirm task is S or M sized. If L, split first.

### During
- Write test stubs first.
- Implement to make tests pass.
- Check each AC as you go.
- Update the current turn stop file if the task pauses or blocks.

### After
- Run tests locally.
- Run quality gates from `docs/QUALITY_GATES.md`.
- Review diff yourself before asking human to review.
- Add to `DONE.md`.
- If you discovered anything, add it to `PARKING_LOT.md`.

## Per-Phase Ritual
1. All tasks in `DONE.md` for that phase?
2. All spec ACs checked off?
3. Run full test suite, record result in `reports/`.
4. Execute all `MANUAL_TESTING.md` flows for the phase.
5. Update `ARCHITECTURE.md` with anything that changed.
6. Write a phase retrospective in `docs/adr/`.
7. Update `README.md` with newly available capabilities.
8. Tag the commit: `git tag phase-N-complete`.
9. Create specs for next phase.
10. Populate `BACKLOG.md` for next phase.

## Weekly Sanity Check
- Is `CONTEXT.md` accurate?
- Is `IN_PROGRESS.md` under 3 tasks?
- Is the latest file in `turns/` still relevant?
- Any items in `PARKING_LOT.md` ready to schedule?
- Does `make test` still pass?

## Doc Update Rules

| When | What to Update |
|---|---|
| Task completed | `DONE.md` + `CONTEXT.md` + `turns/Turn-XX-stop.md` + commit on feature branch |
| Task started | `IN_PROGRESS.md` + `turns/Turn-XX-start.md` |
| Agent turn starts | `turns/Turn-XX-start.md` (include branch, planned tests) |
| Agent turn ends | `turns/Turn-XX-stop.md` (include tests run or N/A) + git commit |
| Material decision | `docs/DECISIONS_LOG.md` |
| Blocker found | `BLOCKED.md` + `turns/Turn-XX-stop.md` |
| Idea surfaces | `PARKING_LOT.md` |
| Phase done | `CONTEXT.md` + `CHANGELOG.md` + tag |
| Manual step done | `ENVIRONMENT.md` |

## ADR Trigger List
Write an ADR whenever a choice would be confusing to a future developer who only
sees the code. Expected ADRs:
- ADR-001: LangGraph over AutoGen
- ADR-002: Option B conversation graph
- ADR-003: LiteLLM for routing
- ADR-004: Supabase over self-hosted Postgres
- ADR-005: e2b vs Docker subprocess for sandbox
- ADR-006: Neo4j over Memgraph
- ADR-007: Temporal for durable workflows
