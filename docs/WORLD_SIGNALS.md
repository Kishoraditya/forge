# World Signals

World signals are small, regularly updated facts that help agents understand
the current project environment without rereading the whole repository.

They are not a substitute for specs or tests. They are routing and validation
signals.

## Signal Types

| Signal | Source | Update When | Purpose |
|---|---|---|---|
| Current branch | `git branch --show-current` | Every task start | Avoid work on wrong branch |
| Remote freshness | `git fetch origin` + rebase status | Before edits and before merge | Detect simultaneous branch updates |
| Active task | `tasks/IN_PROGRESS.md` | Task start/end | Preserve scope |
| Feature registry | `docs/FEATURES.md` | Feature added/renamed | Prevent invented feature IDs |
| Latest turn | `turns/` | Every agent response | Crash recovery |
| Environment readiness | `docs/CONTEXT.md` + `.env.local` presence | Human gate/task start | Know which integrations can run |
| Quality gate status | Test/lint command output | Before review/merge | Validate correctness |
| Dependency surface | `pyproject.toml`, frontend package files | Dependency changes | Detect governance needs |
| External docs freshness | Official docs lookup date in task notes | API/library uncertainty | Avoid stale integration assumptions |

## Agent Start Checklist

At the start of implementation work, capture:
- Branch name
- Active task ID
- Feature ID
- Latest turn file
- Allowed files
- Required tests
- Whether live credentials are required

## Branch Sync Signals

Before editing:

```bash
git fetch origin
git status
git branch --show-current
```

Before merge:

```bash
git fetch origin
git checkout main
git pull --ff-only origin main
git checkout feat/FXXX-short-name
git rebase main
```

If `git fetch` shows remote updates on shared files, rebase before continuing
and rerun quality gates.

## Validation Signals

Each task stop file should record:
- Tests run
- Lint/type checks run
- Commands skipped and why
- Files changed
- Any world signal that changed the next action

## Dynamic External Signals

For unstable external facts such as library APIs, provider behavior, pricing,
or cloud-service setup screens, agents must verify against official sources
before encoding assumptions into specs or implementation.
