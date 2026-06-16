# Prompt — Implementation

Your task: [paste from tasks/IN_PROGRESS.md]

Read before editing:
1. `AGENTS.md`
2. `docs/CONVENTIONS.md`
3. Relevant spec file
4. Files listed under "Context required"

State implementation acknowledgment:
- Spec file read
- Task ID
- Files allowed / forbidden
- Test plan

Rules:
- Work on branch from task (`feat/FXXX-short-name`)
- Write failing test first, then implement
- Max 300 lines/file, 50 lines/function
- Developer signature header on every new file
- No business logic in API routes
- No direct DB calls outside `backend/app/db/`
- No direct LLM provider calls — use LiteLLM
- Update `turns/Turn-XX-stop.md` when pausing or finishing
