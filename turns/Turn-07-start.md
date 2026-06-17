# Turn-07 Start - 2026-06-17

## Branch
`feat/F001-scaffolding`

## Task
Fix npm ci on Linux CI (emnapi lock sync), add local CI check script/Makefile target.

## Tests
- `cd frontend && npm ci && npm run lint && npm run build`
- `make ci-check` (new)
