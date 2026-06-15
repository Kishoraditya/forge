# Human Tasks

Tasks assigned to the human developer. These cannot be delegated to AI agents.

Principle: complete HT-001 through HT-008 before asking AI agents to create
Phase 0 specs or implementation tasks. These steps establish review, rollback,
local tooling, frontend scaffold, the first hosted database target, and one live
LLM provider. Everything after HT-008 stays deferred until feature code exists
that can consume and test it.

---

## Human Bootstrap Gate - Complete Before AI Project Work

### HT-001 - Initialize Git Repository
**Priority**: P0
**Status**: not started
**Estimated**: 5 min
**Run after automated task**: Scaffold is complete.
**Blocks**: Safe review, commits, rollback, and all later automated work.

```bash
git init
git add .
git commit -m "chore: initialize forge project structure and governance docs"
```

---

### HT-002 - Review & Approve Scaffold
**Priority**: P0
**Status**: not started
**Estimated**: 30 min
**Run after automated task**: HT-001 initial commit.
**Blocks**: AI-assisted Phase 0 spec drafting.

- Open the file tree and verify structure
- Check `CLAUDE.md`, `AGENTS.md`, and `docs/CONVENTIONS.md` read sensibly cold
- Check `tasks/HUMAN_TASKS.md` reflects the actual human workflow
- Fix anything that looks wrong manually
- Commit: `git add . && git commit -m "chore: reviewed project scaffold"`

---

### HT-003 - Create Local Environment File
**Priority**: P0
**Status**: not started
**Estimated**: 10 min
**Run after automated task**: HT-002 scaffold approval.
**Blocks**: Local process startup, settings parsing, and future integration tests.

Copy `.env.example` to `.env.local`.

Required now:
- `ENVIRONMENT=development`
- `DEBUG=True`
- Local Redis URL if Redis is run locally
- Local Neo4j values if Neo4j is run locally

Keep unused provider and observability variables as placeholders until a task
explicitly targets them.

---

### HT-004 - Install Local Tooling
**Priority**: P0
**Status**: not started
**Estimated**: 15 min
**Run after automated task**: HT-003 `.env.local`.
**Blocks**: Running tests, linters, scripts, and generated project scaffolds.

```bash
pip install poetry
poetry install
pre-commit install
```

Install Node 20+ and Docker Desktop if they are not already available.

---

### HT-005 - Initialize Frontend App
**Priority**: P0
**Status**: not started
**Estimated**: 15 min
**Run after automated task**: HT-004 tooling install.
**Blocks**: Frontend specs/tasks that expect a real Next.js app to exist.

```bash
cd frontend
npx create-next-app@latest . --typescript --tailwind --app
npx shadcn-ui@latest init
```

Commit the generated frontend scaffold separately after review.

---

### HT-006 - Verify Local Prerequisites
**Priority**: P0
**Status**: not started
**Estimated**: 10 min
**Run after automated task**: HT-005 frontend scaffold.
**Blocks**: AI agents running local checks without rediscovering machine setup issues.

Verify these commands are available:
- `python --version`
- `poetry --version`
- `node --version`
- `npm --version`
- `docker --version`
- `git status`

Do not require `make dev` yet. That comes after the Docker Compose/local-dev
task creates the actual dev stack.

---

### HT-007 - Provision Supabase Project
**Priority**: P0
**Status**: not started
**Estimated**: 15 min
**Run after automated task**: HT-006 local prerequisite check.
**Blocks**: BYOK storage, session persistence, schema work, and later integration tests.

1. Go to [supabase.com](https://supabase.com) and create a project
2. Copy the project URL to `SUPABASE_URL`
3. Copy the anon key to `SUPABASE_ANON_KEY`
4. Copy the service role key to `SUPABASE_SERVICE_ROLE_KEY`
5. Enable pgvector so Phase 0 schema work is not blocked later:
   `CREATE EXTENSION IF NOT EXISTS vector;`

Do not create production/staging Supabase projects yet. One development project
is enough for the first AI-assisted phase.

---

### HT-008 - Get One LLM Provider API Key
**Priority**: P0
**Status**: not started
**Estimated**: 10 min
**Run after automated task**: HT-007 Supabase project setup.
**Blocks**: Live BYOK validation and end-to-end LLM smoke testing.

Obtain one provider key only. Anthropic is the default recommendation, but any
provider supported by LiteLLM is acceptable.

Do not add every BYOK provider key now. Keep unused provider variables as
placeholders until a test explicitly targets that provider.

After HT-008 is complete, AI agents can start Phase 0 spec creation and task
breakdown.

---

## Deferred Human Tasks - Schedule When Feature Code Needs Them

### HT-009 - Verify Local Dev Stack
**Priority**: P0 when scheduled; otherwise deferred
**Status**: not started
**Estimated**: 15 min
**Run after automated task**: After the F001 Docker Compose/local-dev task creates `infra/docker/docker-compose.dev.yml` and `make dev` wiring.
**Blocks**: Manual local smoke testing.

Run `make dev` and verify only the services implemented at that point:
- Backend responds at `http://localhost:8000/health` once the health route exists
- Frontend loads at `http://localhost:3000` once the Next.js app exists
- Redis connects if the current task uses Redis
- Neo4j browser loads at `http://localhost:7474` if the current task uses Neo4j

---

### HT-010 - Provision Neo4j AuraDB
**Priority**: P1 until graph persistence is scheduled
**Status**: not started
**Estimated**: 10 min
**Run after automated task**: After the first graph persistence task that cannot be satisfied by local Neo4j, such as F009/F031 hosted graph integration testing.
**Blocks**: Hosted graph database smoke tests and deployment parity.

Use local Neo4j from Docker for earlier development.

---

### HT-011 - Provision Upstash Redis
**Priority**: P1 until hosted Redis is scheduled
**Status**: not started
**Estimated**: 10 min
**Run after automated task**: After Redis-backed Celery/rate-limit/session features exist and before hosted integration or deployment testing.
**Blocks**: Hosted Redis smoke tests and deployment parity.

Use local Redis from Docker for earlier development.

---

### HT-012 - Get e2b Sandbox API Key
**Priority**: P1 until sandbox execution is scheduled
**Status**: not started
**Estimated**: 10 min
**Run after automated task**: After F017/F018 sandbox execution code exists; before cloud sandbox integration tests.
**Blocks**: e2b-backed tool execution tests.

Keep `E2B_API_KEY` as a placeholder until this task is scheduled. Use the local
Docker fallback for earlier implementation where possible.

---

### HT-013 - Set Up Observability Accounts
**Priority**: P2 until observability features are scheduled
**Status**: not started
**Estimated**: 30 min
**Run after automated task**: After the relevant Phase 2 observability task exists: F022 for Opik, F023 for PostHog, F030 for Sentry, or F042 for GrowthBook.
**Blocks**: Hosted observability dashboards and alerts.

Create only the account needed by the scheduled feature:
- Sentry DSN to `SENTRY_DSN`
- PostHog key to `POSTHOG_API_KEY`
- Opik key to `OPIK_API_KEY`
- GrowthBook key to `GROWTHBOOK_API_KEY`

Do not create all observability accounts on Day 0.
