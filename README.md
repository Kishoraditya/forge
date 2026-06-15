# 🔥 Forge

**A self-hosted, BYOK, multi-session AI agent workbench.**

Forge is a composable AI agent harness that lets you bring your own LLM API keys and run a full-featured agent workbench on free-tier infrastructure. Designed for single-admin deployments with multiple anonymous simultaneous users — session-isolated, credit-limited, zero-login. Built on a conversation graph architecture from day one.

---

## ✨ Key Features

- **BYOK (Bring Your Own Key)** — Anthropic, OpenAI, Google, Mistral, DeepSeek, OpenRouter, HuggingFace
- **Multi-Session** — Multiple anonymous users with full session isolation and per-session credit limits
- **Conversation Graph** — Option B graph architecture with Neo4j for branching, forking, and revisiting conversations
- **Agent Orchestration** — LangGraph + DSPy pipelines with planning, execution, and review nodes
- **Tool Ecosystem** — MCP protocol support, custom tools, sandboxed code execution via e2b
- **Human-in-the-Loop** — Configurable guardrails and approval workflows for sensitive operations
- **Full Observability** — OpenTelemetry traces, Opik LLM monitoring, PostHog analytics, GrowthBook feature flags
- **Globally Deployable** — Docker + Terraform + Cloudflare Tunnel on Railway / free-tier infra
- **Investor-Demonstrable** — Production-grade architecture ready for enterprise evaluation

---

## 🛠 Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js 14, Tailwind CSS, shadcn/ui, Zustand |
| API Gateway | FastAPI, Cloudflare Tunnel, CORS |
| Agent Core | LangGraph, DSPy, LiteLLM |
| Tools | MCP Protocol, Custom Tools, e2b Sandboxed Exec |
| Control Plane | Guardrails, Policy Engine, Human-in-Loop |
| Async Tasks | Celery, Redis, Temporal |
| Persistence | Supabase (PostgreSQL + pgvector), Neo4j |
| Observability | OpenTelemetry, Opik, PostHog, GrowthBook |
| Infrastructure | Docker, Terraform, Cloudflare, Railway |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 20+
- Docker & Docker Compose
- Poetry (`pip install poetry`)

### Setup
```bash
# Clone the repository
git clone https://github.com/your-org/forge.git
cd forge

# Copy environment template
cp .env.example .env.local

# Complete human bootstrap gate before AI-assisted work
# See tasks/HUMAN_TASKS.md HT-001 through HT-008

# Install backend dependencies once Poetry is available
poetry install

# Initialize frontend during HT-005
cd frontend
npx create-next-app@latest . --typescript --tailwind --app
npx shadcn-ui@latest init
```

See [tasks/HUMAN_TASKS.md](tasks/HUMAN_TASKS.md) for the bootstrap gate and
[docs/ENVIRONMENT.md](docs/ENVIRONMENT.md) for environment setup. `make dev`
is available after the local Docker Compose task creates the dev stack.

---

## 📁 Project Structure

```
forge/
├── backend/
│   ├── app/
│   │   ├── api/           # FastAPI route handlers
│   │   ├── core/          # LangGraph agent flows, DSPy modules
│   │   ├── services/      # Business logic layer
│   │   ├── models/        # Pydantic schemas
│   │   ├── db/            # Database access (Supabase)
│   │   ├── graph/         # Neo4j graph operations
│   │   └── tools/         # MCP tools, sandboxed execution
│   └── tests/             # Test suite
├── frontend/              # Next.js 14 application
├── infra/                 # Docker, Terraform, Cloudflare
├── specs/                 # Feature specifications
├── tasks/                 # Task tracking
├── docs/                  # Architecture, conventions, guides
├── CLAUDE.md              # AI agent context (Claude Code)
├── AGENTS.md              # AI agent context (Codex / others)
└── Makefile               # Development commands
```

---

## 🔄 Development Workflow

```
forge.md → spec file → human review → tasks → test first → implement → review → done
```

1. Every feature starts with a spec in `specs/phase-X/`
2. Specs are reviewed by a human before work begins
3. Tasks are broken out from the spec into `tasks/`
4. Tests are written before implementation
5. `docs/CONTEXT.md` is updated after every completed task

See [docs/CONVENTIONS.md](docs/CONVENTIONS.md) for coding standards and [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for system design.

---

## 📄 License

MIT — see [LICENSE](LICENSE) for details.

---

## 📊 Status

**Phase 0 — Active Development**

Project scaffold complete. Core engine implementation beginning. See [docs/CONTEXT.md](docs/CONTEXT.md) for current state.
