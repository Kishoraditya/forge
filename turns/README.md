# Turn Files

This folder stores crash-recovery notes for agent sessions.

Use one zero-padded turn number per response:
- `Turn-00-start.md`
- `Turn-00-stop.md`
- `Turn-01-start.md`
- `Turn-01-stop.md`

The start file is the first repo action in a response. The stop file is the last
repo action in a response. When resuming after a crash, read the newest file in
this folder first.

## Required Turn Fields

**Start file**: branch name, task ID(s), planned test commands.

**Stop file**: tests run (command + pass/fail) or `Tests: not required — [reason]`,
files changed summary, commit hash after turn commit.

## Commit Rule

Every completed turn is committed on a feature branch before the session ends.
Never commit directly to `main`. See `docs/GIT_WORKFLOW.md`.
