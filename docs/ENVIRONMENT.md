# FORGE — Environment & Operations Setup
<!-- Environment version: 1.0.0 | Author: claude-code + KSR | Date: 2026-06-12 -->

This guide contains checklists and references for manual environment setup, API keys, external service configurations, and multi-environment parity.

---

## 1. First-Time Setup Checklist

Complete the bootstrap environment steps before AI-assisted Phase 0 spec/task
work begins. After HT-008, add new hosted services only when the matching
feature task needs them.

- [ ] **Copy Environment Template**:
  ```bash
  cp .env.example .env.local
  ```
- [ ] **Provision One Supabase Development Project**:
  Add `SUPABASE_URL`, `SUPABASE_ANON_KEY`, and `SUPABASE_SERVICE_ROLE_KEY`.
- [ ] **Add One LLM Provider Key**:
  Add one provider key only, preferably `ANTHROPIC_API_KEY`. Keep unused BYOK provider variables as placeholders.
- [ ] **Keep Later Services Deferred**:
  Leave hosted Neo4j AuraDB, Upstash, e2b, and observability keys as placeholders until `tasks/HUMAN_TASKS.md` schedules them.
- [ ] **Run Bootstrap Script**:
  ```bash
  bash scripts/bootstrap.sh
  ```
- [ ] **Pin Python 3.12 for Poetry** (required — 3.14 breaks dependencies):
  ```bash
  poetry env use python3.12
  poetry install
  ```
- [ ] **Verify Stack is Live**:
  ```bash
  make dev
  ```
  Verify only the services implemented at that point.

---

## 2. API Keys Reference Table

Configure the following variables inside `.env.local`. Bootstrap requires one
Supabase development project and one LLM provider key. Other hosted services can
stay as placeholders until scheduled.

| Key | Where To Get | Env Var Name | Required |
|-----|-------------|--------------|----------|
| **Anthropic API Key** | console.anthropic.com | `ANTHROPIC_API_KEY` | Yes (default model provider) |
| **OpenAI API Key** | platform.openai.com | `OPENAI_API_KEY` | Optional (BYOK support) |
| **Google AI Key** | aistudio.google.com | `GOOGLE_API_KEY` | Optional (BYOK support) |
| **Mistral API Key** | console.mistral.ai | `MISTRAL_API_KEY` | Optional (BYOK support) |
| **DeepSeek API Key** | platform.deepseek.com | `DEEPSEEK_API_KEY` | Optional (BYOK support) |
| **OpenRouter API Key** | openrouter.ai | `OPENROUTER_API_KEY` | Optional (BYOK support) |
| **HuggingFace Token** | huggingface.co/settings/tokens | `HUGGINGFACE_API_KEY` | Optional (BYOK support) |
| **Supabase URL** | Supabase Project Settings | `SUPABASE_URL` | Yes |
| **Supabase Anon Key** | Supabase Project Settings | `SUPABASE_ANON_KEY` | Yes |
| **Supabase Service Role Key** | Supabase Project Settings | `SUPABASE_SERVICE_ROLE_KEY` | Yes |
| **Neo4j URI** | AuraDB Instance Settings | `NEO4J_URI` | Yes |
| **Neo4j Username** | AuraDB Instance Settings | `NEO4J_USERNAME` | Yes |
| **Neo4j Password** | AuraDB Instance Settings | `NEO4J_PASSWORD` | Yes |
| **Redis URL** | Upstash Console | `REDIS_URL` | Yes |
| **Redis Token** | Upstash Console | `REDIS_TOKEN` | Yes |
| **Sentry DSN** | Sentry Project Settings | `SENTRY_DSN` | Optional |
| **PostHog Key** | PostHog Project Settings | `POSTHOG_API_KEY` | Optional |
| **e2b API Key** | e2b.dev Dashboard | `E2B_API_KEY` | Optional (for cloud sandbox) |
| **Opik API Key** | comet.com Console | `OPIK_API_KEY` | Optional (for LLM traces) |

---

## 3. External Service Manual Steps

### Supabase Setup
1. Go to the SQL Editor on your Supabase dashboard.
2. Ensure you have the `vector` extension enabled:
   ```sql
   CREATE EXTENSION IF NOT EXISTS vector;
   ```
3. Apply standard project DDL tables (managed via Alembic when migrations start).

### Neo4j AuraDB Setup
1. Create a free AuraDB instance.
2. Note down the credentials and Boltop URI.
3. Ensure firewalls allow connectivity from local dev networks.

### Upstash Redis
1. Choose "Redis" in the Upstash console.
2. Select standard eviction configurations or configure for Celery Broker compatibility.
3. Ensure memory caps align with free-tier limits.

### e2b Code Execution Sandbox
1. Register at [e2b.dev](https://e2b.dev).
2. Retrieve your `E2B_API_KEY`.
3. If using local fallback instead, ensure Docker is running with host isolated limits.

---

## 4. Multi-Environment Parity Table

Ensure environment variable bindings match per environment guidelines:

| Env Var | Development | Staging | Production | Notes |
|---|---|---|---|---|
| `ENVIRONMENT` | `development` | `staging` | `production` | Sets log levels and CORS policies. |
| `DEBUG` | `True` | `False` | `False` | Disables interactive debug loops in prod. |
| `SUPABASE_URL` | Dev Project | Staging Project | Production Project | Session mapping data isolation. |
| `REDIS_URL` | Local / Upstash Dev | Upstash Staging | Upstash Production | Shared broker vs isolated queues. |

---

## 5. Secrets Rotation Protocol

- **Anthropic / OpenAI API Keys**: Rotate annually or immediately if leaked. Use Supabase Vault management.
- **Supabase Service Role Key**: High risk. Guard this carefully. If rotated, update client deployment secrets simultaneously to prevent gateway downtime.
- **Neo4j password**: Rotate if credentials file is misplaced.

---

## 6. Known Manual Gotchas

*(Add manual troubleshooting tricks and environment friction points here as they are discovered during development)*
