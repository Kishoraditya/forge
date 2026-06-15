## prompt 1

dont code just yet, plan
agent is basicallly harness and llm
but instead of very advanced harness, I want to start by simpler one, it will have vector db for RAG, graph if required, multiple skills, personalities, system prompts, few apis and tools as MCP -- thats it -- byok open source hosted agent -- is this good enough

## PROMPT 2

BYOK, MCP tools easy connect, normal tools (custom tools installable in environment, or custom python scripts, etc), webhooks, websockets, apis, RAG, vector db, skills, personalities, execution environment, query breakdown, prompt directory with dspy, oberservability, tracing, monitoring, logging, temporal, feature flags, LLM infernece (openrouter, huggingface, gemini, openai, claude, deepseek, etc) , only conversation memory, -- session ends, context ends, with a pdf/json of whole conversation available for download, -- for simpler context management at this initial stage, no user logins right now, just single admin logging -- all hosted via free resources for now, managed via terrraform, clouflare, etc -- so even though open source, its easy to use gloabally, human in loop, query breakdown and manual approaval, sandboxed code execution, context engineering, -- all basics built in python, good frontend, UIUXCX, so its easy to use, supabase, posthog, openteleetry, growthbook, celery, redis, opik, prompt tests, regression tests, benchmarks, tool tests, langgraph, langchain, pydantic, pgvector, docker, tailwind, nextjs, shadcn, litellm and rouuting, conversation graphs, to preserve as much contexxt as possible in form multiple graph views, different entities based multiple views of graph data, graph db, decision logging for self reflection, decsion biases (cognitive and other wise), load ballancer, scalable infra, a non llm output should be possible, after query break down/task creation, planning logic, control logic, policy enforcemenat, guraadrails, pre query filter and prompt optimization, etc

## prompt 3

: "free resources" + "scalable infra" + "load balancer" -- this is just trrue in initial stages -- we dont want to monetize it just right now, we will build this and test extensively across users, who will not be able to login or anything, and every session will have llm api credit limits too to save cost, -- its scalable in the sense if multiple users are trying to use it simultaneously in their own sessions, not collaboratively, load balancer basically built in tandem with terraform to roll up or down as per requirements and cost savings, 

temporal because I want to show capablitity wise to investors before next phase, this is just basic fllow, I have goals for enterprise level innnovation, which will require funds, so now I want this initial vision to be completelly built as I explained, and even add somee more features you suggest which can be huge value add in qualitative manner, and hence we also need option B, 

now just create a complete feature list as I mentioned previously and corresponding stack, in chronological order

Now for all mentioned phases the whole document can act as my goal, how do I use spec kit to develop tasks, and tracking documentations, open source tool,
Such that the tasks are small, one file, function, or module focused such that persistence is not issue for llms, or even manual code review is not an issue,
which is why I want to develop it alone as ai agent first (claude llm, claude code, codex, antigravity, cursor like tools) spec and test driven development, so i can review each impementation cleanly and in checklist format,
Since I am on free instancec for all these tools, I might need good context on whats done, whats needs to done, from start itself in living document within folder itself, along with rituals, formatting (developer signature, docstrings, comments, etc) , structure, context, architecture, manual steps to follow (env files, keys apis, etc) , manual testing (so commplete frontend + backend simulataneous flows) , automated testing reports, readme, and also add applications of this state and future features and scope beyond the ones mentioned, a smmarized context from where a new agent can know where to navigate for what -- so it will develop its own contexxt, etc
Also makee it human led, to save tokens some very easy tasks can be done on the side by human, and update accordingly
Dont create tasks directy, give frameowrk, tell step by step how to get started with speckit to develop such form of development, any prompt or structure you would suggest, am i missing anything in this approach? assume I juust have a folder named "forge", and in it is a folder caled docs, andd in it it is a file called forge.md as the plan you have given above

## prompt 4

Read docs/forge.md and docs/FORGE_DEV_FRAMEWORK.md in full before doing anything.



Your job is to build the project scaffold only — no product code.



Do the following in order:



1. Create every folder listed in the "Complete Folder Structure" section of 

   FORGE_DEV_FRAMEWORK.md. Add a .gitkeep in empty folders.



2. Create these files with real content (not placeholders) — use the templates 

   and examples defined in FORGE_DEV_FRAMEWORK.md:

   - CLAUDE.md

   - AGENTS.md

   - .cursorrules

   - README.md (brief, 1 page)

   - Makefile

   - docs/ARCHITECTURE.md

   - docs/CONVENTIONS.md

   - docs/CONTEXT.md (initial state — nothing built yet)

   - docs/ENVIRONMENT.md (env var table from forge.md tech stack)

   - docs/MANUAL_TESTING.md (empty structure, headers only)

   - docs/SCOPE.md (copy future scope section from FORGE_DEV_FRAMEWORK.md)

   - docs/RITUALS.md (copy rituals section from FORGE_DEV_FRAMEWORK.md)

   - docs/adr/ADR-000-template.md

   - specs/_template.spec.md

   - tasks/_format.md

   - tasks/BACKLOG.md (empty, just headers)

   - tasks/IN_PROGRESS.md (empty)

   - tasks/DONE.md (empty)

   - tasks/BLOCKED.md (empty)

   - tasks/PARKING_LOT.md (empty)

   - tasks/HUMAN_TASKS.md (seeded with Day 0 human tasks from framework doc)

   - tasks/THIS_WEEK.md (empty)

   - CHANGELOG.md (v0.0.0 entry only)

   - scripts/create_spec.sh

   - scripts/create_task.sh

   - scripts/bootstrap.sh

   - scripts/context_refresh.sh

   - .github/PULL_REQUEST_TEMPLATE.md

   - pyproject.toml (poetry, with all deps from forge.md master stack)

   - .gitignore

   - .pre-commit-config.yaml



3. After all files are created, show me a tree of what was built.



Do not create any backend/, frontend/, or infra/ code files yet.

Do not install any packages yet.

Only create the governance and scaffolding layer.
Also check docs/workflow.md
Add anything if can be beneficial, do not reduce anything already mentioned

