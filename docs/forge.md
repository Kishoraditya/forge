FORGE — BYOK Open-Source Agent Platform
Complete Feature List, Tech Stack & Build Phases
Vision: A self-hosted, BYOK, multi-session AI agent workbench — composable harness + LLM, globally deployable on free infrastructure, investor-demonstrable, enterprise-architecture-ready.
Audience at this stage: Single admin, multiple anonymous simultaneous users (session-isolated, credit-limited). No logins. No persistence between sessions. Everything built for Option B conversation graph from day one.

Table of Contents
Architecture Overview
Master Tech Stack
Phase 0 — Core Engine
Phase 1 — Agent Intelligence Layer
Phase 2 — Observability & Control Plane
Phase 3 — Graph, Memory & Self-Reflection
Phase 4 — Investor Demo Layer
Phase 5 — Hardening & Scale
Suggested Value-Add Features
Hosting Strategy
Infrastructure & IaC
Testing Strategy

Architecture Overview
┌─────────────────────────────────────────────────────────────┐
│                        FRONTEND LAYER                       │
│         Next.js 14 + Tailwind + shadcn/ui + Zustand         │
├─────────────────────────────────────────────────────────────┤
│                       API GATEWAY                           │
│              FastAPI + Cloudflare Tunnel + CORS             │
├──────────────┬──────────────────────────┬───────────────────┤
│  AGENT CORE  │    TOOL & SKILL LAYER    │  CONTROL PLANE    │
│  LangGraph   │  MCP + Custom Tools +    │  Guardrails +     │
│  + DSPy +    │  Sandboxed Exec +        │  Policy Engine +  │
│  LiteLLM     │  Webhooks + WebSockets   │  Human-in-Loop    │
├──────────────┴──────────────────────────┴───────────────────┤
│                     ASYNC TASK LAYER                        │
│               Celery + Redis + Temporal                     │
├─────────────────────────────────────────────────────────────┤
│                    PERSISTENCE LAYER                        │
│        Supabase (PostgreSQL + pgvector) + Neo4j/Memgraph    │
├─────────────────────────────────────────────────────────────┤
│                  OBSERVABILITY LAYER                        │
│          OpenTelemetry + Opik + PostHog + GrowthBook        │
├─────────────────────────────────────────────────────────────┤
│                     INFRA LAYER                             │
│          Docker + Terraform + Cloudflare + Railway          │
└─────────────────────────────────────────────────────────────┘


Master Tech Stack
Core Runtime
Component
Tool
Version/Notes
Language
Python
3.11+
API Framework
FastAPI
Async-native, OpenAPI auto-docs
Data Validation
Pydantic v2
All state schemas, tool I/O
Agent Orchestration
LangGraph
Conversation + task graphs
LLM Abstractions
LangChain
Tool wrappers, chains
Prompt Optimization
DSPy
Prompt directory, teleprompters
LLM Routing
LiteLLM
100+ providers, BYOK

Frontend
Component
Tool
Notes
Framework
Next.js 14
App router
Styling
Tailwind CSS
Utility-first
UI Components
shadcn/ui
Accessible, themeable
State Management
Zustand
Lightweight
Graph Visualization
React Flow
Conversation/task DAG
Charts & Analytics
Recharts
Session metrics
Real-time
Socket.io client
Agent streaming
Code Editor
Monaco Editor
Tool scripting in-browser

Data & Persistence
Component
Tool
Notes
Primary DB
Supabase (PostgreSQL 15)
Auth, sessions, config
Vector Search
pgvector (via Supabase)
RAG embeddings
Graph DB
Neo4j AuraDB Free / Memgraph
Conversation + entity graphs
Cache
Redis (Upstash free tier)
Session state, semantic cache
Object Storage
Supabase Storage
Session exports, tool artifacts
ORM
SQLAlchemy async + Alembic
Migrations

Async & Workflow
Component
Tool
Notes
Task Queue
Celery
Async tool execution
Message Broker
Redis
Celery backend
Durable Workflows
Temporal
Long-running, investor demo
WebSockets
FastAPI WebSocket
Real-time agent streaming

LLM Providers (via LiteLLM)
Provider
Models
Notes
Anthropic
Claude 3.5 Sonnet/Haiku
Default recommended
OpenAI
GPT-4o, GPT-4o-mini
BYOK
Google
Gemini 1.5 Pro/Flash
BYOK
Mistral
Mistral Large/Small
BYOK
DeepSeek
DeepSeek V2
Low cost option
OpenRouter
Any model
Meta-router
HuggingFace
Open models
Free tier inference
Ollama
Local models
Self-hosted option

Observability
Component
Tool
Notes
Telemetry Spine
OpenTelemetry
Traces, metrics, logs
LLM Tracing
Opik (Comet)
Prompt lineage, eval
Product Analytics
PostHog
Session analytics
Feature Flags
GrowthBook
Self-hosted
Error Tracking
Sentry (free tier)
Exception monitoring
Uptime
BetterStack (free)
Endpoint health

Security & Control
Component
Tool
Notes
Guardrails
Guardrails AI
Output validation
Prompt Injection Detection
Rebuff / custom
Pre-query filter
Rate Limiting
SlowAPI + Redis
Per-session throttling
Secrets
Supabase Vault
BYOK key storage
Sandbox
e2b / Docker subprocess
Code execution isolation

Infrastructure
Component
Tool
Notes
Containers
Docker + Docker Compose
Local + prod parity
IaC
Terraform
All infra as code
CDN + Tunnel
Cloudflare
Free global routing
Backend Hosting
Railway (free tier)
Auto-deploy
Frontend Hosting
Cloudflare Pages
Free, global CDN
Load Balancing
Cloudflare + Terraform
Auto-scale rules
CI/CD
GitHub Actions
Free tier

Testing
Component
Tool
Notes
Unit Tests
pytest + pytest-asyncio
Core logic
API Tests
httpx + FastAPI TestClient
Endpoint coverage
Frontend Tests
Playwright
E2E
LLM Evals
Opik + custom benchmarks
Prompt regression
Tool Tests
pytest-mock
Tool call simulation
Load Tests
Locust
Concurrent session simulation


Phase 0 — Core Engine (Weeks 1–3)
Goal: Working end-to-end loop. Query in → LLM processes → response out. Everything else builds on this foundation.
F001 — Project Scaffolding & Monorepo
Python monorepo: /backend, /frontend, /infra, /scripts, /tests, /docs
Docker Compose: backend, frontend, redis, supabase-local, neo4j
.env.example with all required keys documented
Makefile with make dev, make test, make deploy commands
Pre-commit hooks: Black, Ruff, isort, mypy
Stack: Docker, Python 3.11, Node 20, Make
F002 — BYOK Configuration System
Admin UI page for entering and validating API keys per provider
Keys stored encrypted in Supabase Vault (never in env files in prod)
Per-provider health check endpoint (validates key is live before saving)
Model alias system: admin defines fast, smart, cheap → maps to any provider model
LiteLLM config auto-generated from alias definitions
Stack: LiteLLM, Supabase Vault, FastAPI, Pydantic
F003 — LLM Routing & Inference Core
LiteLLM proxy as internal service
Streaming support (SSE) for all providers
Automatic retry with exponential backoff
Fallback chain: if primary model fails → secondary → tertiary
Provider-level rate limit tracking
Cost per token calculation per provider stored in config
Stack: LiteLLM, Redis (rate limit counters), Pydantic
F004 — Session Management
Anonymous session creation on page load (UUID, no login)
Session stored in Supabase: id, created_at, model_used, token_count, status
Per-session API credit budget: admin sets global default (e.g., $0.10/session)
Real-time token counter displayed in UI
Hard stop at budget limit: graceful message, no silent failure
Session expiry: configurable TTL (default 2 hours inactivity)
Stack: Supabase, Redis (session state), FastAPI, Zustand
F005 — Basic Conversation Interface
Chat UI: message stream, typing indicator, model badge
Markdown rendering in responses (code blocks, tables, lists)
Copy-to-clipboard per message
Message timestamps
Regenerate last response button
Clear conversation button (with confirmation)
Stack: Next.js, shadcn/ui, Tailwind, Socket.io
F006 — Single Admin Authentication
Supabase Auth for single admin account only
Admin dashboard route (protected)
Public-facing routes are fully open (no login required for users)
Session token + Supabase RLS policies enforce admin-only data access
Stack: Supabase Auth, Next.js middleware, JWT
F007 — Basic RAG Foundation
Document upload in admin panel (PDF, TXT, MD, CSV)
Chunking pipeline: LangChain RecursiveCharacterTextSplitter
Embedding model: configurable (OpenAI ada-002, Cohere, HuggingFace local)
Storage: pgvector in Supabase
Retrieval: cosine similarity top-k, configurable k
Retrieved chunks injected into system prompt context window
Stack: LangChain, pgvector, Supabase, LiteLLM (embeddings)
F008 — Supabase Schema Foundation
Tables: sessions, messages, tools, skills, personalities, prompts, decisions, graph_nodes, graph_edges, api_keys, credit_ledger, feature_flags
RLS policies: admin full access, public read-only on session_id-scoped rows
Migrations managed via Alembic
Stack: Supabase, PostgreSQL, Alembic, SQLAlchemy

Phase 1 — Agent Intelligence Layer (Weeks 4–6)
Goal: The system starts behaving like an agent, not just a chatbot. Query breakdown, planning, tool use, and skill/personality switching go live.
F009 — LangGraph Conversation Graph (Option B)
Every conversation is a LangGraph StateGraph
State schema (Pydantic): messages, current_task, tools_used, decisions_made, entities_extracted, graph_node_refs, session_meta
Graph nodes: input_router, pre_filter, planner, executor, reviewer, output_formatter
Every node transition logged as a graph edge in Neo4j
Session graph serialized to JSON on end
Stack: LangGraph, Pydantic, Neo4j, Supabase
F010 — Query Breakdown & Task Decomposition
Input query analyzed for complexity (single-step vs multi-step)
Multi-step queries decomposed into ordered subtask list
Each subtask gets: id, description, required_tools, estimated_tokens, dependencies
Subtask plan rendered in UI as collapsible step list before execution
Admin can configure decomposition model (often cheaper/faster model)
Stack: LangGraph, LiteLLM, Pydantic, React Flow (UI)
F011 — Human-in-Loop Approval Gate
After task decomposition, execution can be paused for admin/user approval
Three modes: auto-execute, approve-each-step, approve-plan-only
Approval UI: show full plan, tool calls intended, estimated cost, approve/reject/edit
Rejected steps can be re-prompted with user instruction
Approval decisions logged to decisions table
Stack: LangGraph (interrupt nodes), Supabase, WebSocket, shadcn/ui
F012 — Planning & Control Logic
Pre-execution planner node: selects tools, orders steps, estimates token budget
Control loop: after each step, evaluates whether to continue, retry, or escalate to human
Retry policy: configurable max retries per step, backoff strategy
Escalation triggers: tool failure, confidence below threshold, token budget >80% consumed
Stack: LangGraph, Pydantic, Redis (retry counters)
F013 — Skill System
Skills are named bundles: system_prompt_fragment + tool_list + config_overrides
Stored in Supabase skills table with versioning (semver)
Skills can be stacked (multiple active simultaneously)
Admin UI: create, edit, enable/disable, version skills
Skills loaded at session init based on URL param or admin default
Example skills: code-reviewer, data-analyst, research-assistant, creative-writer
Stack: Supabase, FastAPI, LangGraph (state injection), shadcn/ui
F014 — Personality System
Personalities are system prompt presets with parameter overrides (temperature, top_p, max_tokens)
Stored in Supabase personalities table
Includes: name, description, system_prompt, model_overrides, tone_tags
Admin can create custom personalities; a set of defaults shipped
Active personality displayed in chat header
Personality can be switched mid-session (new context window segment)
Stack: Supabase, LiteLLM, LangGraph, shadcn/ui
F015 — DSPy Prompt Directory
All system prompts and few-shot examples stored as DSPy signatures
Prompt versioning: every change creates a new version, old versions preserved
Prompt testing: run a stored prompt against a test input set, compare outputs
Teleprompter support: admin can trigger DSPy optimization pass on any prompt
Active prompt version per skill/personality tracked in Supabase
Stack: DSPy, Supabase, FastAPI, Pydantic
F016 — MCP Tool Integration
MCP client built into backend (uses official MCP Python SDK)
Admin UI: add MCP server by URL + optional auth header
Tool discovery: on connection, enumerate available tools, store in tools table
Tool schema auto-displayed in UI (name, description, input schema)
MCP connections persisted in Supabase (reconnect on restart)
Pre-bundled MCP servers: filesystem, web search, GitHub, Slack, Postgres
Stack: MCP Python SDK, FastAPI, Supabase, shadcn/ui
F017 — Custom Python Tool Scripts
Admin can write Python tool scripts in browser (Monaco editor)
Scripts stored in Supabase, executed in sandboxed environment on call
Tool schema defined in script docstring (parsed by system on save)
Tool test runner: execute against sample input, show output + errors
Script versioning same as prompt versioning
Stack: e2b (cloud sandbox) or Docker subprocess, Monaco Editor, Pydantic, Supabase
F018 — Sandboxed Code Execution Environment
All code execution (tool scripts, LLM-generated code) runs in isolation
e2b as primary (cloud-managed sandbox, has free tier)
Fallback: Docker subprocess with restricted permissions + no network
Execution timeout: configurable (default 30s)
Resource limits: memory cap, CPU cap
Output captured: stdout, stderr, return value, execution time
Stack: e2b, Docker, asyncio subprocess, resource limits
F019 — Webhook & WebSocket Tool Types
Webhooks: admin registers external URLs as tools; agent POSTs structured payload
WebSocket tools: persistent connection to external service; agent sends/receives messages
Both types defined via same tool schema interface as MCP/Python tools
Webhook response parsed and injected into agent context
Retry on webhook failure with configurable retry count
Stack: httpx (async), websockets, FastAPI, Pydantic
F020 — Non-LLM Output Pipeline
After task decomposition, any step can be marked as non_llm: true
Non-LLM steps execute tool directly and return raw result (no LLM processing)
Result types: JSON, table, code output, file, image URL, chart data
Frontend renders result type-appropriately (table renderer, code block, image viewer)
Enables pure data retrieval, calculations, or API calls without token spend
Stack: LangGraph (conditional edges), FastAPI, Pydantic, React renderers

Phase 2 — Observability & Control Plane (Weeks 7–9)
Goal: Full visibility into what the agent is doing, why, and at what cost. Guardrails, policy enforcement, and cost control become operational.
F021 — OpenTelemetry Integration
OTel SDK instrumented on all FastAPI routes, LangGraph nodes, tool calls
Traces exported to: Jaeger (local Docker) or Grafana Cloud free tier (hosted)
Spans include: session_id, model, prompt_tokens, completion_tokens, latency, tool_name
Custom attributes: skill_name, personality_name, query_complexity_score
Stack: opentelemetry-sdk, opentelemetry-instrumentation-fastapi, Jaeger/Grafana
F022 — Opik LLM Tracing
Opik SDK wraps all LiteLLM calls
Per-call logging: prompt version used, model, token counts, latency, cost
Prompt lineage: trace which prompt version → which output → which user rating
Evaluation scores stored per trace (auto + human)
Opik dashboard shows: prompt performance over time, regressions flagged
Stack: Opik (Comet), LiteLLM callbacks, Supabase (eval results)
F023 — PostHog Product Analytics
Events tracked: session_start, query_submitted, tool_called, approval_given, session_end, export_downloaded, credit_limit_hit
Session properties: model_used, skill_active, personality_active, task_count, total_tokens
Funnels: query → decomposition → approval → execution → export
Admin dashboard tab showing PostHog charts embedded
Stack: PostHog (cloud free tier), Next.js PostHog provider, FastAPI event emitter
F024 — GrowthBook Feature Flags
Self-hosted GrowthBook instance in Docker Compose
All Phase 1+ features gated behind flags (enable/disable without redeploy)
Flag types: boolean, string (variant), number
Admin UI: toggle flags in real-time from dashboard
Flag state fetched at session init, stored in Zustand
Example flags: enable_graph_view, enable_temporal_workflows, enable_human_loop, max_session_credits
Stack: GrowthBook (self-hosted), React SDK, FastAPI SDK
F025 — Guardrails & Policy Enforcement
Input guardrails: topic restrictions, PII detection, prompt injection detection
Output guardrails: structured output schema validation, toxicity filter, length limits
Policy rules defined in admin UI as JSON (stored in Supabase)
Policy engine evaluates pre-query (block/allow/modify) and post-output (pass/flag/redact)
Policy violations logged: session_id, rule_triggered, action_taken, original_input_hash
Stack: Guardrails AI, Rebuff (injection detection), Pydantic, Supabase
F026 — Pre-Query Filter & Prompt Optimization
Pre-query pipeline: input → normalize → classify intent → detect injection → apply policy → optimize prompt
Prompt optimization: DSPy rewrite pass to improve clarity before sending to LLM
Intent classification: routes to appropriate skill automatically if admin enables auto-routing
Query complexity scorer (1–5 scale) used to select appropriate model tier
All pre-query transformations logged as a pipeline trace
Stack: DSPy, Rebuff, LangChain, OpenTelemetry, Supabase
F027 — Cost & Token Budget System
Global admin settings: default credit per session ($), max tokens per request, max requests per session
Per-session ledger in Supabase credit_ledger table: debits on each LLM call
Real-time budget display in chat UI (% remaining, estimated calls left)
Pre-execution cost estimate shown before approval (especially for multi-step tasks)
Hard budget enforcement: 80% = warning banner, 100% = graceful stop
Cost breakdown by: model, tool calls, embeddings, completions
Stack: LiteLLM cost tracking, Supabase, Redis (real-time counter), React
F028 — Rate Limiting & Anti-Abuse
Per-session rate limits: requests/minute, tokens/hour
Global rate limits: concurrent sessions cap, requests/minute across all sessions
Redis sliding window counter for rate limit enforcement
Rate limit exceeded: 429 response with retry-after header
Cloudflare WAF rules as outer layer (DDoS, bot detection)
Stack: SlowAPI, Redis, Cloudflare WAF, FastAPI middleware
F029 — Semantic Caching (suggested)
Cache LLM responses by semantic similarity of input (not exact match)
Redis + embedding similarity threshold (configurable, default 0.95)
Cache hit: return stored response instantly (zero token cost)
Cache miss: execute normally, store result
Admin UI: cache hit rate, tokens saved, cache size, flush button
Stack: Redis, pgvector (embedding store), LiteLLM, LangChain cache integration
F030 — Sentry Error Tracking
Backend: all unhandled exceptions captured with full context (session_id, route, payload)
Frontend: React error boundaries report to Sentry
LangGraph node failures: custom Sentry breadcrumbs per node
Alerts: Sentry notifies admin (email/Slack webhook) on new error types
Stack: Sentry (free tier), sentry-sdk Python, @sentry/nextjs

Phase 3 — Graph, Memory & Self-Reflection (Weeks 10–12)
Goal: Conversation becomes a rich structured artifact. Agent starts reasoning about its own decisions. Graph views unlock investor-demo visual power.
F031 — Neo4j Conversation Graph (Option B Full)
Every message, tool call, decision, and entity written to Neo4j in real-time
Node types: Session, Message, Task, ToolCall, Decision, Entity, Skill, Prompt
Edge types: SENT, DECOMPOSED_INTO, CALLED, PRODUCED, REFERENCED, INFLUENCED, FOLLOWED
Bi-directional sync: LangGraph state → Neo4j on every state change
Supabase stores graph_node_id refs in messages table (FK bridge)
Stack: Neo4j AuraDB free, neo4j Python driver, LangGraph callbacks
F032 — Multi-View Conversation Graph UI
React Flow-based graph canvas in frontend
View 1 — Conversation Flow: linear message thread as node DAG
View 2 — Task Graph: task decomposition tree with execution status per node
View 3 — Entity Graph: people, topics, tools, decisions as interconnected nodes
View 4 — Decision Trace: chain of agent decisions with reasoning and confidence
View 5 — Tool Call Graph: which tools were called, in what order, with what results
Toggle between views in sidebar; all share same session graph data
Stack: React Flow, Neo4j, Cypher queries, Zustand, shadcn/ui
F033 — Session Export (PDF + JSON)
On session end (user closes or TTL): serialize full session to JSON
JSON includes: all messages, task graph, tool calls, decisions, entities, token usage, cost, graph snapshot
PDF: formatted conversation transcript with metadata header, tool call summaries
Both available via download button in chat UI and in admin session history
Export triggered server-side; file stored in Supabase Storage (TTL 7 days)
Stack: Supabase Storage, WeasyPrint (PDF), FastAPI background task, Next.js download handler
F034 — Decision Logging & Audit Trail
Every agent decision logged to Supabase decisions table
Fields: session_id, node_name, decision_type, input_summary, output_summary, reasoning_trace, confidence_score, model_used, latency_ms, cost_usd, timestamp
Decision types: route_selection, tool_selection, approval_request, retry, escalate, skip, final_answer
Admin UI: decision log viewer, filterable by session, type, confidence range
Decision log included in session export
Stack: Supabase, LangGraph callbacks, Pydantic, shadcn DataTable
F035 — Cognitive Bias Detection in Decisions (suggested)
Bias detection layer runs post-decision in async background
Checks for: confirmation bias (only tool calls consistent with prior), anchoring (early message dominating plan), recency bias (over-weighting last message), availability heuristic (defaulting to frequently used tool)
Bias flags stored in decisions table: bias_flags: ["confirmation_bias", "anchoring"]
Bias summary shown in session export and decision trace view
Admin UI: bias frequency heatmap across sessions
Stack: Custom Python classifier, Pydantic, Supabase, Recharts (admin viz)
F036 — Agent Self-Critique Loop (suggested)
After agent produces an answer, a lightweight critique pass runs (cheaper model)
Critique checks: completeness, accuracy against retrieved context, instruction adherence, hallucination risk score
If critique score below threshold: agent revises answer (max 1 revision loop)
Critique + original response both stored; UI shows critique score badge
Configurable: enable/disable per personality, critique model, threshold
Stack: LangGraph (critique node), LiteLLM (separate model call), Pydantic, Supabase
F037 — Entity Extraction & Linking
After each message: extract entities (people, places, companies, concepts, dates, tools)
Entities linked across the session graph (same entity in message 2 and message 8 = same node)
Entity disambiguation: simple fuzzy matching + embedding similarity
Entity panel in UI: sidebar listing all extracted entities with message refs
Entities written to Neo4j and Supabase (entity table with session_id)
Stack: spaCy / Gliner, Neo4j, pgvector, LangChain extraction chain
F038 — Conversation Branching (suggested)
User can fork conversation at any message point
Fork creates new session with history up to that point copied
Both branches exist independently; admin can compare them side by side
Branch metadata stored: parent_session_id, fork_point_message_id
UI: branch indicator in message thread, "Fork here" button on hover
Stack: Supabase (session + branch tables), LangGraph (state copy), Next.js routing
F039 — Session Replay (suggested)
Admin can replay any past session (loaded from export JSON)
Replay mode: re-execute with different model, different skill, different prompt version
Side-by-side comparison: original vs replay responses
Enables prompt regression testing and model comparison
Replay sessions get is_replay: true flag, excluded from analytics by default
Stack: Supabase Storage (session JSON), LangGraph (state replay), FastAPI, React diff view

Phase 4 — Investor Demo Layer (Weeks 13–15)
Goal: System tells a compelling story. Temporal workflows, long-running tasks, capability demonstrations that show enterprise-readiness.
F040 — Temporal Workflow Integration
Temporal server in Docker Compose (local) and Temporal Cloud free tier (hosted)
Temporal workflows for: multi-day research tasks, scheduled report generation, periodic RAG refresh, long-horizon agent loops
Each Temporal workflow corresponds to a LangGraph subgraph
Workflow status visible in admin dashboard (running, completed, failed, waiting)
Human-in-loop approval integrated: Temporal Signal used for async approval
Stack: Temporal (Python SDK), LangGraph, FastAPI, Supabase
F041 — Multi-Step Long-Horizon Task Demo
Demo workflow: "Research X topic, summarize findings, write report, generate action plan"
Executes across multiple LLM calls, tool uses, and approval gates
Full graph visualization shows the entire execution tree
Temporal ensures durability: survives server restart mid-task
Designed specifically as investor-facing demo with pre-loaded scenario
Stack: Temporal, LangGraph, DSPy, React Flow
F042 — Prompt A/B Testing (suggested)
Admin can configure two prompt variants for any skill
GrowthBook routes sessions to variant A or B
PostHog tracks: which variant, task completion rate, user satisfaction (thumbs up/down)
Statistical significance computed after N sessions
Winner can be promoted to default with one click
Stack: GrowthBook, PostHog, Opik, Supabase, FastAPI
F043 — Cost Dashboard for Investors
Admin dashboard page: real-time cost breakdown
Charts: cost by model, cost by skill, cost by session, cost over time
Token efficiency score: useful_output_tokens / total_tokens_spent
Semantic cache savings: $ saved by cache hits
Projected monthly cost at current usage rate
Export as PDF for investor materials
Stack: Supabase, Recharts, FastAPI, WeasyPrint
F044 — Live Observability Demo View
Public-safe read-only "observatory" view (no sensitive data)
Shows: active sessions count, tasks in flight, tool calls/minute, model distribution
Real-time updates via WebSocket
Designed as investor-facing "mission control" demo screen
All metrics anonymized: no session content visible
Stack: FastAPI WebSocket, Supabase, Recharts, Next.js
F045 — API-First External Interface
Public REST API for the agent (documented with OpenAPI/Swagger)
Endpoints: POST /session/create, POST /session/{id}/message, GET /session/{id}/status, GET /session/{id}/export
API key auth for external callers (admin generates keys in UI)
Rate limiting applied per API key
Enables third-party integrations and demonstrates enterprise API capability
Stack: FastAPI, Supabase (api_keys table), SlowAPI, OpenAPI

Phase 5 — Hardening & Scale (Weeks 16–18)
Goal: The system is stable, tested, and ready for real user traffic. Infrastructure scales with Terraform. Test coverage is comprehensive.
F046 — Terraform Infrastructure Complete
Full Terraform modules: Cloudflare (DNS, WAF, Pages, Tunnel), Railway (backend services), Upstash (Redis), Neo4j AuraDB, Supabase (project + tables)
Environment configs: dev, staging, prod workspaces
Auto-scale rules in Railway: scale up on CPU >70%, scale down on CPU <20%
Load balancing: Cloudflare Load Balancer with health check failover
One-command deploy: terraform apply -var-file=prod.tfvars
Stack: Terraform, Cloudflare provider, Railway provider, GitHub Actions
F047 — Comprehensive Test Suite
Unit tests: all Pydantic models, utility functions, tool schemas (>80% coverage)
Integration tests: full LangGraph flows with mocked LLM calls
API tests: all FastAPI endpoints (httpx TestClient)
E2E tests: Playwright scenarios (new session → query → tool call → export)
LLM eval tests: Opik-based prompt regression suite (golden dataset)
Tool tests: each MCP tool and custom tool with mock I/O
Load tests: Locust simulating 50 concurrent sessions
Stack: pytest, pytest-asyncio, httpx, Playwright, Locust, Opik
F048 — Prompt Regression Testing
Golden dataset: 50 curated (input, expected_output) pairs per skill
Run on every prompt version change (CI/CD gate)
Metrics: semantic similarity score, task completion rate, instruction adherence
Regression alert: if score drops >5% from baseline, block promotion
Results stored in Supabase, visualized in Opik
Stack: DSPy, Opik, GitHub Actions, Supabase, sentence-transformers
F049 — Security Hardening
Supabase RLS: every table has row-level policies enforced
API input sanitization: all endpoints sanitized via Pydantic + custom validators
CORS: strict allowlist, no wildcard in prod
Cloudflare WAF: OWASP rule set enabled, rate limiting at edge
Secrets rotation: Supabase Vault with rotation reminders
Dependency audit: pip-audit + npm audit in CI/CD
Stack: Supabase RLS, FastAPI middleware, Cloudflare WAF, GitHub Actions
F050 — Admin Dashboard Complete
Overview page: active sessions, cost today, error rate, top skills used
Session browser: list all sessions, search, filter by date/model/skill, view detail
Prompt manager: all DSPy prompts, versions, test runner
Tool manager: MCP connections, custom scripts, test runner
Decision log: all agent decisions, bias flags, audit trail
Cost analytics: full PostHog + Supabase cost dashboards
Feature flags: GrowthBook controls
Config: BYOK keys, model aliases, guardrail policies, credit limits
Stack: Next.js, shadcn/ui, Recharts, Tailwind, Supabase

Suggested Value-Add Features
These are additions beyond your original spec that would meaningfully differentiate Forge for investors and enterprise conversations. Recommend incorporating into phases above.
S001 — Confidence Score as First-Class Output (Phase 1)
Every agent response includes a calibrated confidence score (0.0–1.0). Displayed as a badge in UI. Low confidence responses automatically trigger a disclaimer or escalation. Logged in decisions table. This is a core enterprise differentiator — most agents don't expose uncertainty. Stack: Custom calibration layer on LangGraph output node, Pydantic.
S002 — Tool Call DAG Visualization (Phase 3)
Real-time animated visualization of tool calls as they execute. Nodes = tools, edges = data flow between calls. Shows parallel vs sequential execution. Visible during execution, not just after. Demo-worthy for investors watching live. Stack: React Flow, WebSocket, LangGraph callbacks.
S003 — Pre-Execution Cost Estimate (Phase 2)
Before executing any multi-step task: estimate total cost (tokens × price), time (based on step count + model latency benchmarks), and tool calls. Show as a "receipt" in the approval gate. User can approve or ask for a cheaper execution plan. Stack: LiteLLM cost data, LangGraph plan metadata, React.
S004 — Prompt Injection Audit Log (Phase 2)
Every detected injection attempt logged: session_id, input_hash, attack_type, action_taken (blocked/sanitized/passed), detection_confidence. Admin can review injection attempts in dashboard. Shows platform is enterprise-security-aware. Stack: Rebuff, Supabase, PostHog event.
S005 — Shareable Skill/Personality Bundles (Phase 4)
Export any skill or personality as a YAML bundle (no sensitive data). Import YAML to deploy to another Forge instance. Foundation for a future community marketplace. Demonstrates ecosystem thinking to investors. Stack: PyYAML, Pydantic, Supabase, FastAPI.
S006 — Agent Reasoning Transparency Mode (Phase 3)
Toggle in UI: "Show reasoning" — expands chain-of-thought for each agent step. Shows: what the agent considered, what it rejected, why it chose this tool/response. Stored as part of decision log. Massive UX differentiator for trust and explainability. Stack: LangGraph (verbose mode), React collapsible, Supabase.
S007 — Benchmark Leaderboard (Phase 5)
Admin can run standardized benchmark tasks against any combination of model + skill + prompt version. Results stored in Supabase benchmark table. Leaderboard view shows: model, score, latency, cost per benchmark. Enables model selection decisions with data. Stack: Custom benchmark runner, Opik, Supabase, Recharts.
S008 — Dark Mode + Keyboard Shortcuts (Phase 1)
Dark mode (Tailwind dark class, persisted in localStorage). Keyboard shortcuts: Cmd+Enter submit, Cmd+K command palette, Cmd+/ toggle sidebar, Cmd+E export session. Command palette (like Linear) for power users. Stack: shadcn/ui, Tailwind, cmdk (command palette library).

Hosting Strategy
Free Tier Architecture
Cloudflare Pages (free)       → Next.js frontend
Cloudflare Tunnel (free)      → Secure ingress to Railway backend
Railway (free tier: 5$/mo credit) → FastAPI + Celery worker
Upstash Redis (free: 10k cmd/day) → Cache + rate limiting
Supabase (free: 500MB DB)     → PostgreSQL + pgvector + auth + storage
Neo4j AuraDB (free: 200k nodes) → Graph DB
e2b (free: 100 runs/day)      → Sandboxed code execution
Temporal Cloud (free: 5M actions/mo) → Durable workflows
GrowthBook (self-hosted on Railway) → Feature flags
PostHog (free: 1M events/mo)  → Analytics
Opik (free tier)              → LLM tracing
Sentry (free: 5k errors/mo)   → Error tracking
BetterStack (free)            → Uptime monitoring
GitHub Actions (free: 2k min/mo) → CI/CD

Scale-Up Path (one terraform apply)
When free tiers hit limits: Railway → dedicated instance, Supabase → Pro ($25/mo), Upstash → Pay-as-you-go, Neo4j → AuraDB Professional. All managed by Terraform — no manual re-configuration.

Infrastructure & IaC
Terraform Module Structure
/infra
  /modules
    /cloudflare        → DNS, Pages, WAF, Tunnel, Workers
    /railway           → Services, env vars, scaling rules
    /supabase          → Project, tables (via API), storage buckets
    /upstash           → Redis database
    /neo4j             → AuraDB instance
    /temporal          → Temporal Cloud namespace
  /environments
    /dev               → dev.tfvars
    /staging           → staging.tfvars
    /prod              → prod.tfvars
  main.tf
  variables.tf
  outputs.tf

Cloudflare Configuration
Pages: auto-deploy from GitHub on push to main
Tunnel: routes api.forge.your-domain.com → Railway backend
WAF: OWASP managed ruleset, rate limit 100 req/min per IP
Workers: optional edge middleware for geo-routing or request pre-processing
Load Balancer: health-check based failover between Railway instances
Docker Compose (local dev)
Services: backend (FastAPI), frontend (Next.js), redis, celery-worker, temporal (local), neo4j, supabase-local (via Supabase CLI), growthbook, jaeger (OTel collector)

Testing Strategy
Test Pyramid
        ┌─────────────────┐
         │   E2E (Playwright)│  ← 10% of tests, highest confidence
         ├─────────────────────┤
         │  Integration (httpx) │  ← 20%, API contracts + DB
         ├───────────────────────┤
         │     Unit (pytest)      │  ← 70%, pure logic, fast
         └───────────────────────┘

LLM-Specific Testing
Prompt regression: golden dataset per skill, run on every prompt change
Model comparison: same task, multiple models, scored outputs
Tool contract tests: each tool called with valid + invalid inputs, responses validated
Hallucination spot-checks: factual queries against known-correct answers
All LLM tests use Opik for logging + scoring
CI/CD Gates
pytest unit + integration (must pass)
mypy type checking (must pass)
ruff linting (must pass)
pip-audit security (warnings allowed, critical blocked)
Prompt regression suite (score drop >5% blocks merge)
Playwright smoke test on staging (must pass before prod deploy)

Feature Count by Phase
Phase
Features
Timeline
Priority
Phase 0 — Core Engine
F001–F008
Weeks 1–3
Must ship
Phase 1 — Agent Intelligence
F009–F020
Weeks 4–6
Must ship
Phase 2 — Observability & Control
F021–F030
Weeks 7–9
Must ship
Phase 3 — Graph & Self-Reflection
F031–F039
Weeks 10–12
High value
Phase 4 — Investor Demo
F040–F045
Weeks 13–15
Investor-critical
Phase 5 — Hardening
F046–F050
Weeks 16–18
Stability
Suggested Value-Adds
S001–S008
Woven into phases
Differentiators
Total
58 features
18 weeks




Document version: 1.0.0 — Initial planning spec Next artifact: Architecture Decision Records (ADRs) + P0 detailed component diagram
