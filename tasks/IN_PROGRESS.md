# In Progress

**Branch**: `feat/F006-admin-auth`

---

### P0-F006-001 through P0-F006-005 — Admin authentication

**Spec**: `specs/phase-0/F006-admin-auth.spec.md`
**Status**: in progress (RLS AC5 deferred to F008-006)

**Tests required**:
```
poetry run pytest backend/tests/unit/test_auth.py backend/tests/integration/test_admin_auth_api.py -v
cd frontend && npm run lint && npm run build
```
