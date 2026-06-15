# Git Workflow

Forge work should happen through feature branches and GitHub review, not direct
commits to `main`.

## Branch Naming

| Work Type | Pattern | Example |
|---|---|---|
| Feature | `feat/FXXX-short-name` | `feat/F004-session-management` |
| Fix | `fix/FXXX-short-desc` | `fix/F004-budget-stop` |
| Docs | `docs/FXXX-short-desc` or `docs/scaffold-short-desc` | `docs/scaffold-context-map` |
| Chore | `chore/short-desc` | `chore/pre-commit-config` |

Group tasks for the same feature on the same feature branch unless the tasks are
independent enough to review separately.

## Start Feature Work

```bash
git fetch origin
git checkout main
git pull --ff-only origin main
git checkout -b feat/FXXX-short-name
```

## Sync Before Continuing

Run this before starting a new task on an existing branch:

```bash
git fetch origin
git rebase origin/main
```

If another simultaneous branch changed shared files, sync before editing:

```bash
git fetch origin
git checkout feat/FXXX-short-name
git rebase origin/main
```

## Push Branch

```bash
git push -u origin feat/FXXX-short-name
```

After a rebase of a branch already pushed:

```bash
git push --force-with-lease
```

## Before Merge

```bash
git fetch origin
git checkout main
git pull --ff-only origin main
git checkout feat/FXXX-short-name
git rebase main
make test
make lint
```

If frontend files changed, also run the frontend checks defined by that feature
task once frontend package scripts exist.

## Merge Rule

Merge only after:
- Task Definition of Done is complete
- Quality gates pass
- Human review approves the PR
- Branch is rebased on latest `main`

Prefer squash merge for small task branches and regular merge for larger
feature branches when preserving task-level commits matters.
