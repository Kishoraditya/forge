FORGE — Development Framework Guide
Spec-Driven, AI-Agent-First, Human-Led Solo Development
Purpose of this document: Not the product spec. Not the tasks. This is the meta-system — how Forge gets built. Read this once carefully, then it runs itself.
Starting assumption: You have forge/docs/forge.md and nothing else. By the end of this guide, your folder is a fully operational development machine.

Table of Contents
Philosophy & Core Principles
Why This Approach Works for Solo AI-Assisted Dev
Complete Folder Structure
The Living Documents System
Step-by-Step: Getting Started (Day 0)
The Spec-First Workflow
Task Format — Atomic, Reviewable, Checklistable
Human vs Agent Split
Rituals — Daily, Per-Task, Per-Phase
Coding Conventions & Developer Signature
AI Agent Prompts & Context Loading
Manual Testing Protocols
Automated Testing & Reports
Context Management Strategy
Future Scope Beyond Current Phases
What You Might Be Missing
Tooling Recommendations

1. Philosophy & Core Principles
The Three Laws of This Framework
Law 1 — One Task, One Thing Every task touches exactly one file, one function, or one clearly bounded module. If you can't describe the task in one sentence without "and", split it.
Law 2 — Context is Infrastructure Documentation is not an afterthought. The living documents are as important as the code. An AI agent should be able to open CLAUDE.md cold and know exactly what to do next without asking a single question.
Law 3 — Spec Before Code No implementation file is written before its spec file exists. The spec is the acceptance criteria. The test is the proof. The code is just the mechanism.
Why Spec-Driven for AI-Assisted Development
When working with LLMs (Claude Code, Cursor, Codex), the biggest failure modes are:
Agent doesn't know what "done" looks like → generates too much or wrong things
Agent loses context mid-task → inconsistent naming, duplicated logic
Agent makes architectural decisions you didn't approve → technical debt
Reviewing AI output is hard when the diff is large → misses bugs
Spec-driven development solves all four:
Spec defines done precisely → agent has a target
CONTEXT.md restores state in <500 tokens → no lost context
Architecture is documented before coding → agent follows, doesn't decide
Tasks are one-file → diffs are small → review is fast

2. Why This Approach Works
The Token Economy Problem
Free-tier AI tools have limited context windows and session lengths. You will hit limits. The framework accounts for this:
CONTEXT.md is always a <500 token summary of current project state
Each spec file is self-contained — no need to load the whole project
Task files are atomic — agent only needs the task + spec + conventions
CLAUDE.md is the universal cold-start file (under 200 lines always)
The Human Review Problem
If an agent writes 500 lines, you cannot review it reliably. If an agent writes 50 lines for one function with a spec you wrote, you can review in 3 minutes.
Target: every agent PR diff is under 100 lines of code + tests.
The Context Drift Problem
Sessions end. Days pass. New agents start. Without a living context system, you spend 30 minutes reconstructing state every time. With this framework:
Open CLAUDE.md
Read tasks/IN_PROGRESS.md
Read the relevant spec file
Start coding
Total context-load time: under 5 minutes, for human or agent.

3. Complete Folder Structure
forge/
│
├── CLAUDE.md                    ← MASTER entry point for Claude Code (always <200 lines)
├── AGENTS.md                    ← Same for Codex / other agents (can differ in tone)
├── .cursorrules                 ← Cursor IDE rules (persistent context per file type)
├── .aider.conf.yml              ← Aider config if used
├── README.md                    ← Public-facing project overview
├── Makefile                     ← Developer shortcuts (make spec, make task, make test)
├── pyproject.toml               ← Python project config
├── package.json                 ← Frontend project config
│
├── docs/
│   ├── forge.md                 ← THE PLAN (source of truth, never edited lightly)
│   ├── ARCHITECTURE.md          ← System design, layer diagram, key decisions
│   ├── CONVENTIONS.md           ← Code style, docstrings, naming, signatures
│   ├── CONTEXT.md               ← Living 1-page project state (updated every session)
│   ├── ENVIRONMENT.md           ← Manual setup: env vars, API keys, local services
│   ├── MANUAL_TESTING.md        ← Step-by-step UI + API test flows per feature
│   ├── SCOPE.md                 ← Future features beyond current phases
│   ├── RITUALS.md               ← Development ceremonies (copy of section 9 here)
│   │
│   └── adr/                     ← Architecture Decision Records
│       ├── ADR-000-template.md
│       ├── ADR-001-langgraph-over-autogen.md
│       ├── ADR-002-option-b-graph.md
│       └── ...
│
├── specs/                       ← One spec file per feature (F001–F050 + S001–S008)
│   ├── _template.spec.md        ← Spec template
│   ├── phase-0/
│   │   ├── F001-scaffolding.spec.md
│   │   ├── F002-byok.spec.md
│   │   └── ...
│   ├── phase-1/
│   ├── phase-2/
│   ├── phase-3/
│   ├── phase-4/
│   └── phase-5/
│
├── tasks/
│   ├── _format.md               ← Task template + instructions
│   ├── BACKLOG.md               ← All unstarted tasks, prioritized
│   ├── IN_PROGRESS.md           ← Max 3 active tasks at once
│   ├── DONE.md                  ← Completed tasks with date + outcome notes
│   ├── BLOCKED.md               ← Stuck tasks with blocker description
│   ├── PARKING_LOT.md           ← Ideas that emerged during dev (not yet scheduled)
│   └── HUMAN_TASKS.md           ← Tasks assigned to human (not AI agent)
│
├── reports/
│   ├── test/                    ← pytest HTML reports, coverage XML
│   ├── benchmark/               ← LLM eval benchmark results
│   ├── lint/                    ← mypy, ruff output
│   └── load/                    ← Locust reports
│
├── backend/                     ← Python FastAPI application
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── api/                 ← Route handlers (one file per domain)
│   │   ├── core/                ← Agent engine, LangGraph, LiteLLM
│   │   ├── tools/               ← MCP, custom tools, sandbox
│   │   ├── models/              ← Pydantic schemas
│   │   ├── db/                  ← Supabase client, migrations
│   │   ├── graph/               ← Neo4j client, graph write logic
│   │   ├── services/            ← Business logic (one file per service)
│   │   └── utils/
│   └── tests/
│       ├── unit/
│       ├── integration/
│       └── conftest.py
│
├── frontend/                    ← Next.js application
│   ├── app/
│   ├── components/
│   ├── lib/
│   ├── hooks/
│   └── tests/
│
├── infra/
│   ├── terraform/
│   │   ├── modules/
│   │   └── environments/
│   └── docker/
│       ├── docker-compose.yml
│       ├── docker-compose.dev.yml
│       └── Dockerfile.*
│
└── scripts/
    ├── bootstrap.sh             ← One-command local setup
    ├── create_spec.sh           ← Scaffold a new spec file from template
    ├── create_task.sh           ← Scaffold a new task from template
    └── context_refresh.sh       ← Helper to remind you to update CONTEXT.md


4. The Living Documents System
These five files are updated continuously. They are not set-and-forget.
4.1 CLAUDE.md — The Cold-Start File
Purpose: Any AI agent opens this first. It answers: what is this project, what is the current state, what are the rules, where do I find things.
Length: Hard cap 200 lines. If it grows beyond that, summarize.
Contents (sections, in order):
# FORGE — Claude Code Context

## What Is This
[2-3 sentences on the project]

## Current Phase & Active Work
Phase: X — [Phase Name]
Active tasks: see tasks/IN_PROGRESS.md
Last updated: [date]

## Architecture in 10 Lines
[The 6-layer diagram from forge.md, abbreviated]

## Where Things Live
- API routes: backend/app/api/
- Agent core: backend/app/core/
- Specs: specs/phase-X/
- Conventions: docs/CONVENTIONS.md
- Task format: tasks/_format.md

## Rules (Non-Negotiable)
1. Read the spec file before writing any code
2. One function/file/module per task
3. All code has docstrings (see CONVENTIONS.md)
4. Write test first, then implementation
5. Update CONTEXT.md and IN_PROGRESS.md when task is done

## Do Not
- Invent architecture not in ARCHITECTURE.md
- Create new dependencies without adding to pyproject.toml and noting in task
- Skip the spec file
- Write more than the task requires

## Quick Commands
make dev        → start all services
make test       → run test suite
make spec F=F001 → scaffold spec for feature F001
make task       → scaffold new task

Update frequency: Start of every new phase, or when major architectural decision is made.

4.2 CONTEXT.md — The Living State
Purpose: A snapshot of where the project is right now. Written for a human or agent that has been away for a week and needs to get back up to speed in under 3 minutes.
Length: Exactly 1 page (under 500 tokens). Never longer.
Contents:
# Project Context — [Date]

## Status
Phase 0 complete. Phase 1 in progress (3/12 features done).

## What Was Just Done
F009 LangGraph conversation graph — core state schema complete.
F010 Query breakdown — decomposition node wired, UI pending.

## What Is In Progress
- F011: Human-in-loop approval gate (agent: backend node done, frontend pending)
- F012: Planning & control logic (not started, depends on F011)

## What's Blocked
- F013 Skill system: blocked on F009 merge (PR #12 open)

## Key Decisions Made This Week
- Chose e2b over Docker subprocess for sandbox (see ADR-005)
- Temporal deferred to Phase 4 (Celery sufficient for Phase 1)

## Environment State
- Local Docker Compose: working
- Supabase: connected (project: forge-dev)
- Neo4j: AuraDB instance live
- LiteLLM proxy: running on :4000

## Next 3 Tasks
1. F011-task-002: Frontend approval gate component
2. F012-task-001: Planner node LangGraph implementation
3. F013-task-001: Skill schema + Supabase table

Update frequency: End of every development session, no exceptions.

4.3 ARCHITECTURE.md — The Decisions Map
Purpose: Explains why the system is built the way it is. Prevents agents from reinventing or contradicting established decisions.
Contents:
The 6-layer diagram (from forge.md, expanded)
Data flow diagrams (how a query travels through the system)
Key technology choices with rationale (not duplicating ADRs, just referencing them)
Module dependency map (what imports what)
Database schema overview (tables, relationships)
Neo4j schema (node types, edge types, properties)
Update frequency: When a new ADR is created, update the relevant section here.

4.4 ENVIRONMENT.md — The Manual Operations Guide
Purpose: Everything a human must do by hand. No agent can do these.
Contents (template):
# Environment Setup & Manual Operations

## First-Time Setup (Do Once)
- [ ] Copy .env.example → .env.local, fill all values
- [ ] Create Supabase project at supabase.com, copy URL + anon key
- [ ] Create Neo4j AuraDB free instance, copy connection string
- [ ] Create Upstash Redis, copy REST URL + token
- [ ] Run `bash scripts/bootstrap.sh`
- [ ] Run `make dev` and verify all containers start

## API Keys Required
| Key | Where To Get | Env Var Name |
|-----|-------------|--------------|
| Anthropic | console.anthropic.com | ANTHROPIC_API_KEY |
| OpenAI | platform.openai.com | OPENAI_API_KEY |
| ... | ... | ... |

## Manual Service Setup
### Supabase
1. Go to SQL editor
2. Run: migrations/001_initial_schema.sql
3. Enable pgvector extension: CREATE EXTENSION vector;
4. ...

### Neo4j AuraDB
1. Create free instance
2. Download credentials file
3. Copy bolt URL to NEO4J_URI in .env

## Recurring Manual Tasks
- Supabase schema migration: `make migrate`
- Neo4j constraint setup: run scripts/neo4j_setup.cypher once
- Rotate API keys: update Supabase Vault via admin UI

## Known Manual Gotchas
- [Add as you discover them during dev]

Update frequency: Every time you discover a manual step. Add it immediately.

4.5 MANUAL_TESTING.md — The Human QA Playbook
Purpose: Reproducible test flows that check full-stack behavior. One section per feature, added when that feature ships.
Format per feature:
## F009 — LangGraph Conversation Graph

### Prerequisites
- Backend running on :8000
- Frontend running on :3000
- Neo4j connected

### Flow 1: Basic Conversation Creates Graph Node
1. Open http://localhost:3000
2. Type "What is LangGraph?" and submit
3. Expected: Response appears, token counter increments
4. Open Neo4j browser → run: MATCH (n:Message) RETURN n LIMIT 5
5. Expected: Message node exists with correct session_id

### Flow 2: Multi-Step Query Decomposes
1. Type "Research quantum computing and write a summary"
2. Expected: Task decomposition panel appears with 2-3 subtasks
3. Click approve
4. Expected: Each subtask executes sequentially, graph grows

### Known Edge Cases
- Empty query: should show validation error, no node created
- Budget exceeded: should stop mid-task, show banner


5. Step-by-Step: Getting Started (Day 0)
This is the literal sequence of steps to go from forge/docs/forge.md to a fully operational development machine. Do these in order, once.
Step 1 — Create the Folder Structure (Human, 10 minutes)
Run this from inside forge/:
# Create all directories
mkdir -p docs/adr specs/phase-{0,1,2,3,4,5} tasks reports/{test,benchmark,lint,load}
mkdir -p backend/app/{api,core,tools,models,db,graph,services,utils}
mkdir -p backend/tests/{unit,integration}
mkdir -p frontend/{app,components,lib,hooks,tests}
mkdir -p infra/{terraform/modules,terraform/environments,docker}
mkdir -p scripts .github/workflows

# Create placeholder files so git tracks empty dirs
find . -type d -empty -exec touch {}/.gitkeep \;

Step 2 — Create the Governance Files (Human or Agent, 30 minutes)
Create these files manually or use Claude to draft them based on this framework:
Priority order:
CLAUDE.md — write this first, it gates everything else
docs/CONVENTIONS.md — code standards before any code is written
tasks/_format.md — task template before any tasks are created
specs/_template.spec.md — spec template before any specs are written
docs/CONTEXT.md — initial state (Phase 0, nothing done)
docs/ARCHITECTURE.md — initial diagram from forge.md
docs/ENVIRONMENT.md — seed with known env vars
.cursorrules — cursor context rules
AGENTS.md — like CLAUDE.md but for Codex
README.md — brief public overview
Prompt to give Claude Code for CLAUDE.md:
Read docs/forge.md carefully. Create CLAUDE.md following the template
in docs/FORGE_DEV_FRAMEWORK.md section 4.1. The project is at Day 0,
Phase 0 not yet started. Hard cap: 200 lines. Include the 6-layer
architecture diagram, folder map, and all non-negotiable rules.

Step 3 — Initialize Git & Tooling (Human, 15 minutes)
git init
git add .
git commit -m "chore: initialize forge project structure and governance docs"

# Python tooling
pip install poetry
poetry init  # follow prompts
poetry add fastapi uvicorn pydantic langchain langgraph litellm dspy-ai
poetry add --group dev pytest pytest-asyncio httpx ruff mypy black pre-commit

# Frontend tooling
cd frontend
npx create-next-app@latest . --typescript --tailwind --app
npx shadcn-ui@latest init

# Pre-commit hooks
pre-commit install

Step 4 — Create the Makefile (Human, 15 minutes)
The Makefile is your command vocabulary. Humans and agents both use it.
# Makefile — Forge Developer Commands

.PHONY: dev test lint spec task context

## Start all local services
dev:
	docker-compose -f infra/docker/docker-compose.dev.yml up

## Run full test suite
test:
	cd backend && poetry run pytest tests/ -v --html=reports/test/report.html

## Run linting + type check
lint:
	cd backend && poetry run ruff check . && poetry run mypy app/

## Scaffold a new spec file (usage: make spec F=F001)
spec:
	bash scripts/create_spec.sh $(F)

## Scaffold a new task (interactive)
task:
	bash scripts/create_task.sh

## Remind yourself to update CONTEXT.md
context:
	bash scripts/context_refresh.sh

## Run manual test flow for a feature (usage: make flow F=F009)
flow:
	@echo "Opening manual test guide for $(F)..."
	@grep -A 50 "## $(F)" docs/MANUAL_TESTING.md | head -50

Step 5 — Create the Spec Template (Human or Agent, 10 minutes)
Create specs/_template.spec.md:
# [FXXX] — [Feature Name]
<!-- Spec version: 1.0.0 | Author: [human/agent] | Date: YYYY-MM-DD -->

## Feature Reference
- **Feature ID**: FXXX
- **Phase**: Phase X
- **Depends on**: [list feature IDs or "none"]
- **Blocks**: [list feature IDs or "none"]
- **Estimated tasks**: N

## What This Does (One Paragraph)
[Plain English description. No jargon. What does a user experience?]

## What This Does NOT Do
[Explicit scope boundaries. Prevents scope creep during implementation.]

## Acceptance Criteria
- [ ] AC1: [specific, testable, binary]
- [ ] AC2: ...
- [ ] AC3: ...

## Data Model
[Pydantic schema or table definition for any new data structures]

## API Contract (if applicable)
[Endpoint, method, request body, response body — exact shapes]

## Files to Create
| File | Type | Purpose |
|------|------|---------|
| backend/app/services/xxx.py | New | ... |
| backend/tests/unit/test_xxx.py | New | ... |

## Files to Modify
| File | Change |
|------|--------|
| backend/app/main.py | Register new router |

## Test Cases
### Happy Path
- Input: ... → Expected output: ...

### Edge Cases
- Empty input → Expected: validation error, no side effects
- Budget exceeded → Expected: graceful stop, log entry

### Should Not Happen
- [What explicitly must NOT be possible after this feature]

## Manual Test Flow
[1-5 step human-executable test. Added to MANUAL_TESTING.md when done.]

## Notes & Assumptions
[Anything uncertain, any tradeoffs made in this spec]

Step 6 — Create the Task Template (Human or Agent, 10 minutes)
Create tasks/_format.md:
# Task Format Guide

## What Is a Task
A task is the smallest deployable unit of work. One task = one atomic change.
It may be a single function, a single file, a single database migration,
a single component, or a single config change. Never more than one thing.

## Task ID Convention
[PHASE]-[FEATURE]-[SEQUENCE]
Example: P0-F001-001, P1-F009-003

## Task File Template (used in BACKLOG.md, IN_PROGRESS.md, DONE.md)

---
### [TASK_ID] — [Short Title]

**Spec**: specs/phase-X/FXXX-name.spec.md
**Assigned to**: [human / claude-code / cursor / codex]
**Status**: [backlog / in-progress / in-review / done / blocked]
**Estimated**: [S = <30min | M = 30-90min | L = 90min+]
**Actual**: [fill when done]

**What to do (one sentence)**:
Create `backend/app/services/session_service.py` with `create_session()` function.

**Acceptance checklist**:
- [ ] File created at correct path
- [ ] Function signature matches spec AC1
- [ ] Docstring present (see CONVENTIONS.md)
- [ ] Unit test written and passing
- [ ] No new imports added without updating pyproject.toml
- [ ] CONTEXT.md updated after completion

**Context needed**:
- Read: specs/phase-0/F004-session-management.spec.md
- Read: docs/CONVENTIONS.md (docstring format)
- Reference: backend/app/models/session.py (Pydantic schema)

**Do not**:
- Implement session expiry (that is P0-F004-003, a separate task)
- Modify database schema (that is P0-F004-001)

**Definition of done**:
`pytest tests/unit/test_session_service.py` passes.
Function is importable. Docstring present.

---

## Rules for Tasks

1. Tasks in IN_PROGRESS.md: maximum 3 at any time
2. A task is not "done" until all checklist items are checked
3. Blocked tasks must have a blocker description
4. Human tasks go in HUMAN_TASKS.md, not the main lists
5. Add to PARKING_LOT.md anything that comes up but isn't scheduled

Step 7 — Create BACKLOG.md from forge.md (Agent, 45 minutes)
This is the first significant agent task. Prompt:
Read docs/forge.md (the full feature plan) and tasks/_format.md carefully.

For Phase 0 features F001 through F008:
1. Create one spec file per feature in specs/phase-0/ using the template
   at specs/_template.spec.md. Fill all sections. Be specific.
   Each spec should have 3-6 acceptance criteria.

2. Break each feature into atomic tasks (each <90 minutes of work for an
   experienced developer). Write each task in tasks/BACKLOG.md using the
   format in tasks/_format.md.

Rules:
- One task = one file or one function or one config or one migration
- Do not write any implementation code
- Do not create any source files
- Only create spec files and add task entries to BACKLOG.md

Start with F001. After F001's spec and tasks, pause and show me the output
before continuing to F002.

Do this one feature at a time. Review each spec before asking for the next. This is the highest-leverage human review point in the whole process.
Step 8 — Set Up Docker Compose (Human, 30 minutes)
Create infra/docker/docker-compose.dev.yml manually. This requires your actual credentials and service choices. The agent cannot do this for you.
Services to include:
backend (FastAPI with hot reload)
frontend (Next.js dev server)
redis (Upstash local or Redis official image)
neo4j (neo4j:5-community image, free)
temporal (temporalio/auto-setup for local dev)
jaeger (jaegertracing/all-in-one for local OTel)
growthbook (growthbook/growthbook)
Supabase: use the Supabase local CLI (supabase start) rather than Docker directly.
Step 9 — You Are Ready
At this point you have:
✅ Full folder structure
✅ CLAUDE.md (agent cold-start file)
✅ CONTEXT.md (initial state)
✅ CONVENTIONS.md (code rules)
✅ Spec template + task template
✅ Phase 0 specs written
✅ Phase 0 backlog populated
✅ Docker Compose working
✅ Git initialized
Pick the first task from tasks/BACKLOG.md. Move it to IN_PROGRESS.md. Load the agent. Hand it the task. Review the output. Repeat.

6. The Spec-First Workflow
Every feature follows this exact sequence. No exceptions.
forge.md (feature entry)
    ↓
Create spec file (specs/phase-X/FXXX-name.spec.md)
    ↓
Human reviews spec — is AC complete? Is scope clear? Is data model right?
    ↓  [edit until yes]
Break spec into atomic tasks → add to BACKLOG.md
    ↓
Pick first task → move to IN_PROGRESS.md
    ↓
Write test file first (test_xxx.py, empty stubs)
    ↓
Agent implements to make tests pass
    ↓
Human reviews diff (should be <100 lines)
    ↓
All task checklist items checked?
    ↓  [if no: fix]
Move task to DONE.md with notes
    ↓
Update CONTEXT.md
    ↓
Pick next task
    ↓
When all tasks for feature done: verify spec ACs are all met
    ↓
Add manual test flow to MANUAL_TESTING.md
    ↓
Feature done ✓


7. Task Format
(Already defined in Step 6 above — this section is the reference version)
Task Sizing Guide
Size
Time
Example
S
<30min
Add a Pydantic model field, write one unit test, update one import
M
30-90min
Write one service function + its test, create one API endpoint
L
90min+
Split this task. If you can't, it's a design problem.

Task Assignment Decision
Task Type
Assign To
Write boilerplate/scaffolding
Agent (Claude Code)
Implement a function from spec
Agent
Write unit tests for a function
Agent
Write integration tests
Agent
Create env files, fill secrets
Human
Make service accounts (APIs)
Human
Review + approve agent output
Human
Manual test flows
Human
Architectural decisions
Human
Docker Compose initial setup
Human
Database migration SQL
Human reviews, agent drafts
ADR writing
Human decides, agent drafts


8. Human vs Agent Split
Human Owns (Never Delegate)
Architecture decisions (which go in ADRs)
Security credentials, API keys, secrets
Code review and merge approval
Spec acceptance criteria definition
"Definition of done" per feature
Manual test execution and sign-off
docs/ENVIRONMENT.md updates (only a human knows what manual steps they took)
Choosing which task to work on next
Deciding when a feature is truly shippable
Agent Owns (Within Guardrails)
Implementation of a single function to a written spec
Test file creation to a written spec
Docstring and comment writing
Scaffolding new files from templates
Spec drafting (human must review before finalizing)
BACKLOG.md task population from specs
Suggesting PARKING_LOT.md items during implementation
Shared (Human reviews agent output)
Spec file creation (agent drafts, human finalizes)
ADR drafts (agent writes, human decides)
CONTEXT.md updates (agent suggests, human approves)
Refactoring tasks
Token-Saving Human Shortcuts
The following are explicitly faster for a human to do directly. Don't invoke an agent for these:
Creating empty files with correct names and imports
Moving a task from BACKLOG to IN_PROGRESS
Updating CONTEXT.md (copy the template, fill it in, takes 3 minutes)
Updating DONE.md (copy the task entry, mark checked, add note)
Running make test and checking if it passes
Filling .env files
Clicking through manual test flows
Committing code (git add . && git commit -m "feat: ...")

9. Rituals
Session Start Ritual (Every Time You Open the Project)
1. Open CONTEXT.md — read in full (3 minutes)
2. Open tasks/IN_PROGRESS.md — what is currently active?
3. If continuing a task: re-read the spec file + task description
4. If starting new: pick from BACKLOG, move to IN_PROGRESS
5. Load agent with: CLAUDE.md + relevant spec + task description
6. Begin

Session End Ritual (Every Time You Close the Project)
1. Is the current task done?
   → Yes: move to DONE.md, check all checklist items, note actual time
   → No: note where you stopped in the task description (IN_PROGRESS.md)
2. Update CONTEXT.md (takes 3-5 minutes, use the template)
3. Run `make test` — note pass/fail in CONTEXT.md
4. Commit everything: `git add . && git commit -m "[type]: what you did"`
5. Check PARKING_LOT.md — any new ideas to add?

Per-Task Ritual
Before:
- Read spec AC list
- Read task "context needed" files
- Confirm task is S or M sized (if L, split first)

During:
- Write test stubs first
- Implement to make tests pass
- Check each AC as you go

After:
- Run tests locally
- Review diff yourself before asking human to review
- Add to DONE.md
- If you discovered anything: add to PARKING_LOT.md

Per-Phase Ritual (When a Phase Is Complete)
1. All tasks in DONE.md for that phase?
2. All spec ACs checked off?
3. Run full test suite, record result in reports/
4. Execute all MANUAL_TESTING.md flows for the phase
5. Update ARCHITECTURE.md with anything that changed
6. Write a phase retrospective in docs/adr/ (ADR-XXX-phase-N-retro.md)
7. Update README.md with newly available capabilities
8. Tag the commit: `git tag phase-N-complete`
9. Create specs for next phase (agent task, human review)
10. Populate BACKLOG.md for next phase


10. Coding Conventions & Developer Signature
Developer Signature
Every file created in this project starts with this header:
# =============================================================================
# forge / [module path]
# =============================================================================
# Description : [one sentence — what this file does]
# Layer       : [Infra | API | Core | Tools | Memory | Observability]
# Feature     : [FXXX — Feature Name]
# Author      : [human | claude-code | cursor | codex] + KSR (reviewed by)
# Created     : YYYY-MM-DD
# Modified    : YYYY-MM-DD
# Version     : 0.1.0
# =============================================================================

For TypeScript/TSX files:
// =============================================================================
// forge / [module path]
// [same fields]
// =============================================================================

Docstring Standard (Python)
def create_session(model_alias: str, credit_budget_usd: float) -> Session:
    """
    Create a new anonymous agent session with token budget tracking.

    Args:
        model_alias: LiteLLM model alias (e.g., 'smart', 'fast', 'cheap')
        credit_budget_usd: Maximum spend allowed for this session in USD

    Returns:
        Session: Newly created session with UUID, expiry, and credit ledger entry

    Raises:
        ValueError: If model_alias not found in LiteLLM config
        BudgetError: If credit_budget_usd is below minimum threshold

    Example:
        >>> session = create_session("fast", 0.10)
        >>> session.id
        'uuid-here'

    Notes:
        - Session is written to Supabase immediately on creation
        - Token counter starts at 0, hard stop enforced at 100% of budget
        - See: specs/phase-0/F004-session-management.spec.md
    """

Naming Conventions
Element
Convention
Example
Python files
snake_case
session_service.py
Python classes
PascalCase
SessionService
Python functions
snake_case
create_session()
Python constants
UPPER_SNAKE
MAX_SESSION_TOKENS
TypeScript files
kebab-case
session-provider.tsx
React components
PascalCase
SessionBudgetBar
API routes
kebab-case
/api/session-create
Env vars
UPPER_SNAKE
SUPABASE_SERVICE_ROLE_KEY
Database tables
snake_case
session_messages
Graph nodes
PascalCase
:Message, :ToolCall
Feature branches
feat/FXXX-short-name
feat/F009-langgraph-graph
Fix branches
fix/FXXX-short-description


Commit messages
Conventional Commits
feat(F009): add message node to neo4j

Structural Rules
Maximum file length: 300 lines. If longer, split into submodules.
Maximum function length: 50 lines. If longer, extract helpers.
No logic in __init__.py files (imports only)
No business logic in API route handlers (delegate to services)
No direct database calls outside db/ layer
No hardcoded strings (use constants or config)
All async functions must be awaited (no fire-and-forget without Celery)

11. AI Agent Prompts & Context Loading
Universal Agent Startup Prompt
Use this as the first message in any new agent session:
I am working on a project called Forge — a self-hosted BYOK AI agent platform.

Please read the following files in this order before doing anything:
1. CLAUDE.md (project overview + rules)
2. docs/CONVENTIONS.md (code standards)
3. tasks/IN_PROGRESS.md (what is currently active)
4. [relevant spec file] (the feature you will implement)
5. [the specific task description] (what exactly to do)

After reading, confirm you understand:
- What the project is
- What the current task is
- What files you will create or modify
- What the acceptance criteria are
- What you must NOT do

Then ask me one question if anything is unclear before starting.
Do not write any code until I confirm your understanding.

Prompt for Spec Creation
Read docs/forge.md section [FXXX — Feature Name].
Read specs/_template.spec.md.

Create specs/phase-X/FXXX-feature-name.spec.md

Rules:
- Be specific and testable in acceptance criteria (binary pass/fail)
- List every file you will create or modify
- Define the exact Pydantic model or API shape
- Scope out anything not in forge.md's description of this feature
- Do not invent requirements

Show me the spec before saving. I will review and approve.

Prompt for Task Breakdown
Read specs/phase-X/FXXX-feature-name.spec.md carefully.
Read tasks/_format.md for the task template.

Break this feature into atomic tasks (each <90 minutes, one file or function).
Write them in task format. Do not write any code.

Rules:
- One task = one file or one function or one migration
- Tasks must be ordered by dependency (cannot start task 3 before task 2)
- Mark which tasks are human tasks vs agent tasks
- Each task must have a one-sentence "what to do" and a done checklist

Output the task list. I will review before adding to BACKLOG.md.

Prompt for Implementation
Your task: [PASTE TASK DESCRIPTION FROM IN_PROGRESS.md]

Context files to read:
- docs/CONVENTIONS.md
- [relevant spec file]
- [files listed in "context needed"]

Rules:
- Write the test file first with stubs
- Then implement to make tests pass
- Follow CONVENTIONS.md exactly (file header, docstrings, naming)
- Do not create any files not listed in the task
- Do not add logic beyond what the task requires
- When done, tell me which files were created/modified and which tests pass

Prompt for CONTEXT.md Update
Based on our session today, update docs/CONTEXT.md.

What we completed: [list tasks]
What is in progress: [list tasks]
What is blocked: [list with reasons]
Key decisions made: [list any]

Keep it under 500 tokens. Use the existing format.
Show me the updated content before I save it.

.cursorrules File Content
# Forge Project — Cursor Rules

## Project Context
Read CLAUDE.md before every file edit. Read docs/CONVENTIONS.md before writing any code.

## File Rules
- All Python files must start with the developer signature header from CONVENTIONS.md
- All functions must have complete docstrings (see CONVENTIONS.md for format)
- Max 300 lines per file, max 50 lines per function

## Behavior Rules
- Only modify files listed in the current task description (tasks/IN_PROGRESS.md)
- If a change requires a new dependency, add it to pyproject.toml AND note it in the task
- Write tests before or alongside implementation, never after separately
- Never create business logic in API route files — put it in services/

## Navigation
- API routes: backend/app/api/
- Business logic: backend/app/services/
- LangGraph flows: backend/app/core/
- Pydantic models: backend/app/models/
- Database: backend/app/db/
- Tests: backend/tests/

## When in Doubt
Read the spec file. The spec is the authority.


12. Manual Testing Protocols
The Two-Terminal Workflow
Always run manual tests with two terminals open:
Terminal 1: make dev (all services running, logs visible)
Terminal 2: your commands, curl calls, database checks
Browser: localhost:3000

Standard Test Flow Per Feature
When a feature is complete, execute this flow and record results in docs/MANUAL_TESTING.md:
Smoke test: Does the UI load? Does the backend respond at /health?
Happy path: Execute the most basic version of the feature
Edge case 1: Empty input or missing required field
Edge case 2: Budget/limit exceeded
Database verification: Check Supabase table for expected rows
Graph verification: Check Neo4j for expected nodes/edges (if applicable)
Log verification: Check Docker logs for expected trace output
Database Check Commands (Keep These Handy)
# Check Supabase (via psql or Supabase dashboard SQL editor)
SELECT * FROM sessions ORDER BY created_at DESC LIMIT 5;
SELECT * FROM messages WHERE session_id = '[uuid]';

# Check Neo4j (via Neo4j browser at localhost:7474)
MATCH (n) RETURN n LIMIT 25;
MATCH (s:Session)-[:CONTAINS]->(m:Message) RETURN s, m LIMIT 10;

# Check Redis (via redis-cli)
redis-cli keys "session:*"
redis-cli get "session:[uuid]:budget"


13. Automated Testing & Reports
Test Structure
backend/tests/
  conftest.py           ← shared fixtures (mock LLM, test DB, mock tools)
  unit/
    test_session_service.py    ← one test file per service file
    test_llm_router.py
    test_skill_loader.py
    ...
  integration/
    test_session_api.py        ← full API endpoint tests with test DB
    test_langgraph_flow.py     ← full LangGraph execution tests
    ...

Test Report Generation
# Generate HTML report + coverage
make test
# Output: reports/test/report.html, reports/test/coverage/

# Run with coverage report
pytest --cov=app --cov-report=html:reports/test/coverage

When to Run Tests
Event
Test Level
After each task
pytest tests/unit/test_[relevant_file].py
Before moving task to DONE
pytest tests/ (full suite)
Before phase completion
Full suite + all integration tests
Before any deploy
Full suite + Playwright E2E

Benchmark & LLM Eval Reports
Store in reports/benchmark/:
Filename format: benchmark-FXXX-YYYY-MM-DD.json
Contents: prompt version tested, model, golden dataset scores, latency
These are referenced in DONE.md for prompt-related features

14. Context Management Strategy
The Context Hierarchy
An AI agent in a new session needs context at different granularities:
Level 1 (always load):  CLAUDE.md         ~150 tokens
Level 2 (always load):  CONTEXT.md        ~400 tokens
Level 3 (task load):    Current task      ~200 tokens
Level 4 (task load):    Relevant spec     ~500 tokens
Level 5 (as needed):    Source files      variable
                        ────────────────────────────
                        Total guided load: ~1,250 tokens

This leaves the majority of the context window for actual implementation, which is the goal.
Rules for Context Efficiency
CLAUDE.md must never exceed 200 lines (ruthlessly summarize)
CONTEXT.md must never exceed 500 tokens (one page)
Task descriptions must be self-contained (no "see other task")
Spec files are the most verbose files — they're read once per feature, not every session
Never paste entire source files into agent context; reference by path and function name
Context Refresh Triggers
Update CONTEXT.md when:
Any task moves to DONE
Any blocker is added or removed
Any key architectural decision is made
At the start of a new phase
After any major refactor
The "Lost Context" Recovery Protocol
If an agent (or you) has no idea what's happening:
1. Read CLAUDE.md → understand the project
2. Read CONTEXT.md → understand current state
3. Read tasks/IN_PROGRESS.md → understand active work
4. Read docs/ARCHITECTURE.md → understand the system
5. Run `git log --oneline -20` → see recent history

This 5-step protocol should fully restore context in under 10 minutes.

15. Future Scope Beyond Current Phases
Document in docs/SCOPE.md. These are not current tasks but should inform architecture decisions made today (don't paint yourself into corners).
Near-Term Extensions (Phase 6+)
Multi-tenant: user accounts, per-user isolated environments
Agent-to-agent collaboration: multiple specialized agents in one session
Shared memory across sessions: user opt-in persistent knowledge base
Agent marketplace: import/export skill + personality bundles as YAML
Prompt marketplace: community-contributed DSPy prompts
Plugin system: third-party tools installable from a registry
Enterprise Path
SSO / SAML: enterprise identity integration
Audit logs: immutable compliance audit trail (separate from decision log)
Role-based access: admin, editor, viewer roles
White-label: deployable as a branded product
On-premise: fully air-gapped deployment option
SLA + monitoring: enterprise uptime guarantees
Data residency: configurable data region per tenant
Research & Innovation Directions
Digital twin agents: per-user/per-employee persistent agent with private memory
Agent alignment monitoring: detect when agent behavior drifts from intent
Adversarial robustness: formal red-teaming of agent pipelines
Multi-modal tools: vision, audio, document understanding as native tool types
Symbolic reasoning harness: hybrid LLM + rule engine for verifiable outputs
Federated agents: agents that can call each other across instances
Agent economics: token budgets as a resource allocation mechanism with market dynamics
TEOL (Temporal Explainability Orchestration Layer): full symbolic trace of all decisions
Platform Extensions
CLI: forge run "task description" from terminal
VS Code extension: Forge as a coding assistant with project context
Browser extension: Forge operating on any webpage
Mobile app: session management and monitoring on the go
Zapier/n8n integration: Forge as a workflow automation node

16. What You Might Be Missing(Add if not already)
Honest assessment of gaps in the current approach:
1. Dependency Graph Between Tasks
Right now tasks are listed but not explicitly linked by dependency. Before starting Phase 0 tasks, add a depends_on: [task_ids] field to each task. This prevents you from accidentally starting F011 before F009 is done.
Add to task format: **Depends on**: [P0-F009-001, P0-F009-002 | none]
2. A "Known Issues" Log
During implementation you will discover bugs, edge cases, and quirks. Without a dedicated place to write them down, they get forgotten. Add tasks/KNOWN_ISSUES.md: date, description, severity, affected feature, workaround if any.
3. Git Branch Strategy
Without a clear branching strategy, you will have merge conflicts and messy history. Simple recommendation: main (stable), develop (active), feat/FXXX-name (per feature). Agent always works on a feature branch. Human merges to develop. Develop merges to main at phase completion.
4. Environment Parity Documentation
Local dev, staging, and prod will diverge silently. Add a table to ENVIRONMENT.md listing every environment variable and marking which environments it applies to. Prevents "works locally, breaks in prod" failures.
5. ADR Trigger List
Architecture Decision Records are only useful if you write them at the right time. Add to RITUALS.md: "Write an ADR whenever you make a choice that would be confusing to a future developer who only sees the code." Keep a list of expected ADRs based on forge.md's key choices (LangGraph over AutoGen, Option B graph, LiteLLM routing, etc.)
6. A "Definition of Shippable" Per Phase
Right now phases complete when tasks complete. But what does "shippable Phase 0" mean? Define explicitly: which manual test flows must pass, what test coverage percentage is required, what performance benchmarks must be met. Add to each phase in forge.md or create a docs/PHASE_GATES.md.
7. Secrets Rotation Reminder
BYOK means users put in API keys. Those keys expire, get compromised, get rotated. Add to ENVIRONMENT.md: a section on secrets hygiene — when to rotate, how to rotate without downtime, which keys are highest risk.
8. A "This Week" Focus
BACKLOG.md can grow overwhelming. Add a tasks/THIS_WEEK.md as a focused weekly pull — max 5 tasks from backlog that you commit to this week. Reduces decision fatigue at session start.
9. Changelog
CHANGELOG.md at root. Updated at every phase completion using Conventional Commits log. This is your investor-facing record of progress velocity.
10. The Agent Handoff Document
When you switch agents mid-task (e.g., start in Claude Code, switch to Cursor), there is no standard handoff. Add a mini-template to IN_PROGRESS.md: "Handoff note: stopped at [function/line], next step is [X], test failing at [Y]."
Al in docs/
vision/vision.md
architecture/system.md
architecture/dataflow.md
architecture/deployment.md
decisions/ADR-001.md
ADR-001

Decision:
Use Postgres

Reason:
Need relational consistency

Alternatives:
Mongo
Neo4j

Status:
Accepted

decisions/ADR-002.md
glossary/terminology.md
standards/coding.md

standards/testing.md
standards/docs.md

onboarding/quickstart.md
Tasks can contain
Goal
Files
Dependencies
Acceptance Criteria
Tests
Status
Reviewer Notes
Context state
Current Sprint

Completed:
- Authentication
- User CRUD

In Progress:
- Agent CRUD

Blocked:
- Keycloak Integration

Next:
- Agent Templates
We can also have repository map or development rituals
RITUAL 1

Before coding

Read:
    current-state.md
    repository-map.md
    active task

After coding

Run:
    tests
    lint

Update:
    task status
    current-state.md

Create:
    completion report
And maybe developer signature like
"""
Module:
Purpose:
Dependencies:

Author: Forge System
Reviewed By:
Status:
"""
Also definition of done
[ ] Code implemented

[ ] Unit tests pass

[ ] Integration tests pass

[ ] Docs updated

[ ] Current state updated

[ ] Manual test updated

[ ] Acceptance criteria met

[ ] Human approved
forge/

    docs/
    tasks/
    reports/
    specs/
    architecture/
    tests/
    scripts/

    .forge/
        workflows/
        prompts/
        templates/
        agents/
Vision
    ↓
Epic
    ↓
Feature
    ↓
Task
    ↓
Test
    ↓
Implementation
    ↓
Review
    ↓
Documentation Update
Create User model

Files:
    users/models.py

Acceptance:
    User can be created
    Email unique
    Unit tests pass

Tests:
    test_user_creation()

17. Tooling Recommendations
For Spec-Driven Task Management (Open Source, Free)
Option A — Pure Markdown (Recommended for Solo) Everything in tasks/ as markdown files. Zero overhead. Git history = audit trail. Works perfectly with AI agents since they read/write markdown natively.
Option B — Linear (Free Tier, Generous) If you want a UI for tasks. Excellent for showing investors "how the project is managed." Create issues from task descriptions. Use labels: agent, human, blocked, phase-X. Keep markdown as source of truth; Linear mirrors it.
Option C — GitHub Issues + Projects Free, native to your repo. Create issue per task. Project board shows kanban. Label conventions: agent-task, human-task, phase-0 through phase-5.
For AI-Assisted Development
Tool
Use Case
Free Tier
Claude Code
Primary agent (best for reasoning + architecture)
Free tier available
Cursor
File-level editing, refactoring, autocomplete
Free tier available
Aider
Terminal-based, git-native, good for precise edits
Fully free, open source
Codex CLI
OpenAI alternative for tasks
Usage-based
Continue.dev
VS Code plugin, multi-model
Free, open source

Recommended combination: Claude Code for spec review + architecture tasks. Cursor for implementation tasks. Aider for precise surgical edits (rename, refactor).
For Context Management
Tool
Purpose
Obsidian (free)
Visual knowledge graph of your docs folder
mdBook (free)
Render your docs/ as a navigable website
Logseq (free)
Linked markdown notes if you prefer that style

For Automated Test Reports
# pytest-html for test reports
pip install pytest-html
pytest --html=reports/test/report.html --self-contained-html

# coverage
pip install pytest-cov
pytest --cov=app --cov-report=html:reports/test/coverage/

# View in browser
open reports/test/report.html


Quick Reference — First 7 Days
Day
Focus
Output
Day 0
Folder structure + governance files
CLAUDE.md, CONVENTIONS.md, templates, Makefile
Day 1
Phase 0 specs (F001-F004)
4 spec files, tasks in BACKLOG.md
Day 2
Phase 0 specs (F005-F008)
4 more spec files, BACKLOG.md complete
Day 2
Docker Compose + env setup (human)
Working make dev
Day 3
F001 scaffolding (first real code)
Repo structure, pyproject.toml, Docker builds
Day 4
F002 BYOK config system
BYOK endpoint, LiteLLM config, admin UI page
Day 5
F003 LLM routing
LiteLLM proxy, streaming, fallback chain
Day 6
F004 Session management
Session create/end, budget tracking, Redis counter
Day 7
F005-F006 (parallel)
Chat UI + admin auth


Document version: 1.0.0
 This is a living document — update the relevant section whenever the process evolves.
 Next: Run Step 1-4 from Section 5. Then use the agent prompt in Section 11 to create Phase 0 specs.
