# Feature Registry

Canonical list of Forge feature IDs. Agents must not invent feature IDs.

## Phase 0 - Core Engine

| ID | Feature | Completion Gate |
|---|---|---|
| F001 | Project Scaffolding & Monorepo | Local project skeleton, commands, and dev-stack spec exist |
| F002 | BYOK Configuration System | Admin can define, validate, and store provider keys safely |
| F003 | LLM Routing & Inference Core | LiteLLM routing, streaming, retry, fallback, and cost accounting work |
| F004 | Session Management | Anonymous sessions, budget enforcement, and TTL work |
| F005 | Basic Conversation Interface | Chat UI supports messages, markdown, copy, regenerate, clear |
| F006 | Single Admin Authentication | Admin-only routes and public anonymous routes are enforced |
| F007 | Basic RAG Foundation | Upload, chunk, embed, store, retrieve, and inject context |
| F008 | Supabase Schema Foundation | Core tables, RLS, migrations, and pgvector are ready |

## Phase 1 - Agent Intelligence Layer

| ID | Feature |
|---|---|
| F009 | LangGraph Conversation Graph |
| F010 | Query Breakdown & Task Decomposition |
| F011 | Human-in-Loop Approval Gate |
| F012 | Planning & Control Logic |
| F013 | Skill System |
| F014 | Personality System |
| F015 | DSPy Prompt Directory |
| F016 | MCP Tool Integration |
| F017 | Custom Python Tool Scripts |
| F018 | Sandboxed Code Execution Environment |
| F019 | Webhook & WebSocket Tool Types |
| F020 | Non-LLM Output Pipeline |

## Phase 2 - Observability & Control Plane

| ID | Feature |
|---|---|
| F021 | OpenTelemetry Integration |
| F022 | Opik LLM Tracing |
| F023 | PostHog Product Analytics |
| F024 | GrowthBook Feature Flags |
| F025 | Guardrails & Policy Engine |
| F026 | Prompt Injection Detection |
| F027 | Cost Dashboard & Budget Controls |
| F028 | Rate Limiting & Anti-Abuse |
| F029 | Semantic Caching |
| F030 | Sentry Error Tracking |

## Phase 3 - Graph, Memory & Self-Reflection

| ID | Feature |
|---|---|
| F031 | Neo4j Conversation Graph Full |
| F032 | Multi-View Conversation Graph UI |
| F033 | Session Export |
| F034 | Decision Logging & Audit Trail |
| F035 | Cognitive Bias Detection |
| F036 | Agent Self-Critique Loop |
| F037 | Entity Extraction & Linking |
| F038 | Conversation Branching |
| F039 | Session Replay |

## Phase 4 - Investor Demo Layer

| ID | Feature |
|---|---|
| F040 | Temporal Workflow Integration |
| F041 | Multi-Step Long-Horizon Task Demo |
| F042 | Prompt A/B Testing |
| F043 | Cost Dashboard for Investors |
| F044 | Live Observability Demo View |
| F045 | API-First External Interface |

## Phase 5 - Hardening & Scale

| ID | Feature |
|---|---|
| F046 | Terraform Infrastructure Complete |
| F047 | Comprehensive Test Suite |
| F048 | Prompt Regression Testing |
| F049 | Security Hardening |
| F050 | Admin Dashboard Complete |

## Phase 0 Exit Criteria

Phase 0 is complete only when:
- [ ] F001 through F008 specs are approved
- [ ] F001 through F008 tasks are done
- [ ] Session creation works
- [ ] Budget tracking works
- [ ] LiteLLM abstraction works with one live provider
- [ ] Supabase schema migrations apply cleanly
- [ ] Conversation UI can send a message and render a response
- [ ] Admin-only configuration is protected
- [ ] Core tests pass
- [ ] Manual demo flow passes
