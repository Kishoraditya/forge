# Prompt — Task Breakdown

Read:
1. Approved spec `specs/phase-X/FXXX-name.spec.md`
2. `tasks/_format.md`

Break the feature into atomic tasks (S or M size; split if L).

Each task must include:
- Task ID: `P0-FXXX-NNN`
- Branch: `feat/FXXX-short-name`
- Files allowed / forbidden
- Depends on: prior task IDs
- Tests required (write test first)
- Definition of done checklist

Add tasks to `tasks/BACKLOG.md` in dependency order. Do not implement code.
