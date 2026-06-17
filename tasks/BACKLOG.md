# Backlog

Prioritized Phase 0 tasks. Implementation order: **F001 → F008 → F006 → F002 → F003 → F004 → F005 / F007**.

Move to `IN_PROGRESS.md` when starting (max 3 active).

---

## F001 — Project Scaffolding & Monorepo
**Spec**: `specs/phase-0/F001-scaffolding.spec.md` | **Branch**: `feat/F001-scaffolding`

### P0-F001-001 — Settings module
**Depends on**: none | **Est**: S | **Assigned**: cursor
**Goal**: Create `backend/app/config.py` loading validated settings from environment.
**Files allowed**: `backend/app/config.py`, `backend/app/constants.py`, `backend/tests/unit/test_config.py`
**Tests**: `pytest backend/tests/unit/test_config.py`

### P0-F001-002 — Application exceptions
**Depends on**: P0-F001-001 | **Est**: S | **Assigned**: cursor
**Goal**: Create `backend/app/core/exceptions.py` with base HTTP-mapped exceptions per `docs/VALIDATION.md`.
**Files allowed**: `backend/app/core/exceptions.py`, `backend/tests/unit/test_exceptions.py`

### P0-F001-003 — Structured logging
**Depends on**: P0-F001-001 | **Est**: S | **Assigned**: cursor
**Goal**: Create `backend/app/core/logging.py` per `docs/LOGGING.md`.
**Files allowed**: `backend/app/core/logging.py`, `backend/tests/unit/test_logging.py`

### P0-F001-004 — Correlation ID middleware
**Depends on**: P0-F001-003 | **Est**: S | **Assigned**: cursor
**Goal**: Create `backend/app/core/middleware.py` adding `X-Correlation-ID` to requests/responses.
**Files allowed**: `backend/app/core/middleware.py`, `backend/tests/unit/test_middleware.py`

### P0-F001-005 — FastAPI app factory
**Depends on**: P0-F001-003, P0-F001-004 | **Est**: M | **Assigned**: cursor
**Goal**: Create `backend/app/main.py` with app factory, middleware, and router registration hook.
**Files allowed**: `backend/app/__init__.py`, `backend/app/main.py`, `backend/app/core/__init__.py`, `backend/tests/unit/test_main.py`

### P0-F001-006 — Health endpoint
**Depends on**: P0-F001-005 | **Est**: S | **Assigned**: cursor
**Goal**: Create `backend/app/api/health.py` with `GET /health`.
**Files allowed**: `backend/app/api/__init__.py`, `backend/app/api/health.py`, `backend/tests/unit/test_health.py`, `backend/tests/integration/test_health_api.py`

### P0-F001-007 — Pytest conftest
**Depends on**: P0-F001-005 | **Est**: S | **Assigned**: cursor
**Goal**: Create `backend/tests/conftest.py` with TestClient fixture and env overrides.
**Files allowed**: `backend/tests/conftest.py`, `backend/tests/unit/.gitkeep`, `backend/tests/integration/.gitkeep`

### P0-F001-008 — Docker Compose dev stack
**Depends on**: P0-F001-005 | **Est**: M | **Assigned**: cursor
**Goal**: Create `infra/docker/docker-compose.dev.yml` (backend, frontend, redis, neo4j).
**Files allowed**: `infra/docker/docker-compose.dev.yml`, `infra/docker/Dockerfile.backend`, `infra/docker/Dockerfile.frontend`

### P0-F001-009 — Alembic bootstrap
**Depends on**: P0-F001-001 | **Est**: M | **Assigned**: cursor
**Goal**: Initialize Alembic with baseline empty migration.
**Files allowed**: `backend/alembic.ini`, `backend/alembic/env.py`, `backend/alembic/versions/001_baseline.py`, `backend/tests/integration/test_alembic_baseline.py`

---

## F008 — Supabase Schema Foundation
**Spec**: `specs/phase-0/F008-supabase-schema.spec.md` | **Branch**: `feat/F008-supabase-schema`

### P0-F008-001 — Async database session
**Depends on**: P0-F001-009 | **Est**: M | **Assigned**: cursor
**Goal**: Create `backend/app/db/session.py` and `base.py` with async SQLAlchemy engine.
**Files allowed**: `backend/app/db/__init__.py`, `backend/app/db/session.py`, `backend/app/db/base.py`, `backend/tests/unit/test_db_session.py`

### P0-F008-002 — Core ORM models (sessions, messages)
**Depends on**: P0-F008-001 | **Est**: M | **Assigned**: cursor
**Goal**: Create session and message SQLAlchemy + Pydantic models.
**Files allowed**: `backend/app/models/__init__.py`, `backend/app/models/common.py`, `backend/app/models/session.py`, `backend/app/models/message.py`, `backend/tests/unit/test_models_session.py`

### P0-F008-003 — Config ORM models (api_keys, ledger, flags)
**Depends on**: P0-F008-001 | **Est**: M | **Assigned**: cursor
**Goal**: Create api_keys, credit_ledger, feature_flags models.
**Files allowed**: `backend/app/models/api_key.py`, `backend/app/models/credit_ledger.py`, `backend/app/models/feature_flag.py`

### P0-F008-004 — Document ORM models
**Depends on**: P0-F008-001 | **Est**: S | **Assigned**: cursor
**Goal**: Create documents and document_chunks models with vector column.
**Files allowed**: `backend/app/models/document.py`, `backend/tests/unit/test_models_document.py`

### P0-F008-005 — Core schema migration
**Depends on**: P0-F008-002, P0-F008-003, P0-F008-004 | **Est**: M | **Assigned**: cursor
**Goal**: Create `002_core_schema.py` migration with all tables and pgvector extension.
**Files allowed**: `backend/alembic/versions/002_core_schema.py`

### P0-F008-006 — RLS policies migration
**Depends on**: P0-F008-005 | **Est**: M | **Assigned**: cursor
**Goal**: Create `003_rls_policies.py` with admin and session-scoped policies.
**Files allowed**: `backend/alembic/versions/003_rls_policies.py`

### P0-F008-007 — Migration integration test
**Depends on**: P0-F008-006 | **Est**: S | **Assigned**: cursor
**Goal**: Integration test applying migrations against dev/test Supabase.
**Files allowed**: `backend/tests/integration/test_migrations.py`

---

## F006 — Single Admin Authentication
**Spec**: `specs/phase-0/F006-admin-auth.spec.md` | **Branch**: `feat/F006-admin-auth`

### P0-F006-001 — Backend JWT dependency
**Depends on**: P0-F001-006 | **Est**: M | **Assigned**: cursor
**Goal**: Create `backend/app/core/auth.py` with `require_admin` FastAPI dependency.
**Files allowed**: `backend/app/core/auth.py`, `backend/tests/unit/test_auth.py`

### P0-F006-002 — Admin me endpoint
**Depends on**: P0-F006-001 | **Est**: S | **Assigned**: cursor
**Goal**: Create `backend/app/api/admin_auth.py` with `GET /api/admin/me`.
**Files allowed**: `backend/app/api/admin_auth.py`, `backend/tests/integration/test_admin_auth_api.py`

### P0-F006-003 — Supabase frontend clients
**Depends on**: none | **Est**: M | **Assigned**: cursor
**Goal**: Add Supabase browser/server clients and `@supabase/supabase-js` dependency.
**Files allowed**: `frontend/lib/supabase/client.ts`, `frontend/lib/supabase/server.ts`, `frontend/package.json`, `frontend/package-lock.json`

### P0-F006-004 — Admin login page
**Depends on**: P0-F006-003 | **Est**: M | **Assigned**: cursor
**Goal**: Create `/admin/login` page with email/password auth.
**Files allowed**: `frontend/app/admin/login/page.tsx`, `frontend/app/admin/layout.tsx`

### P0-F006-005 — Next.js middleware protection
**Depends on**: P0-F006-004 | **Est**: M | **Assigned**: cursor
**Goal**: Create `frontend/middleware.ts` protecting `/admin/*` routes.
**Files allowed**: `frontend/middleware.ts`

---

## F002 — BYOK Configuration System
**Spec**: `specs/phase-0/F002-byok.spec.md` | **Branch**: `feat/F002-byok`

### P0-F002-001 — BYOK Pydantic schemas
**Depends on**: P0-F008-003 | **Est**: S | **Assigned**: cursor
**Goal**: Create `backend/app/models/byok.py` request/response schemas.
**Files allowed**: `backend/app/models/byok.py`, `backend/tests/unit/test_byok_models.py`

### P0-F002-002 — API key repository
**Depends on**: P0-F008-003 | **Est**: M | **Assigned**: cursor
**Goal**: Create `backend/app/db/api_key_repository.py` with encrypted storage.
**Files allowed**: `backend/app/db/api_key_repository.py`, `backend/tests/unit/test_api_key_repository.py`

### P0-F002-003 — BYOK service
**Depends on**: P0-F002-002 | **Est**: M | **Assigned**: cursor
**Goal**: Create `backend/app/services/byok_service.py` validate-and-store via LiteLLM.
**Files allowed**: `backend/app/services/byok_service.py`, `backend/tests/unit/test_byok_service.py`

### P0-F002-004 — Model alias service
**Depends on**: P0-F008-003 | **Est**: M | **Assigned**: cursor
**Goal**: Create `backend/app/services/model_alias_service.py`.
**Files allowed**: `backend/app/services/model_alias_service.py`, `backend/tests/unit/test_model_alias_service.py`

### P0-F002-005 — LiteLLM config generator
**Depends on**: P0-F002-003, P0-F002-004 | **Est**: M | **Assigned**: cursor
**Goal**: Create `backend/app/services/litellm_config_service.py`.
**Files allowed**: `backend/app/services/litellm_config_service.py`, `backend/tests/unit/test_litellm_config_service.py`

### P0-F002-006 — Admin BYOK API routes
**Depends on**: P0-F002-005, P0-F006-001 | **Est**: M | **Assigned**: cursor
**Goal**: Create `backend/app/api/admin_byok.py` and register router.
**Files allowed**: `backend/app/api/admin_byok.py`, `backend/app/main.py`, `backend/tests/integration/test_admin_byok_api.py`

### P0-F002-007 — Admin BYOK UI
**Depends on**: P0-F002-006, P0-F006-005 | **Est**: M | **Assigned**: cursor
**Goal**: Create `frontend/app/admin/byok/page.tsx`.
**Files allowed**: `frontend/app/admin/byok/page.tsx`, `frontend/lib/api/admin-byok-client.ts`

---

## F003 — LLM Routing & Inference Core
**Spec**: `specs/phase-0/F003-llm-routing.spec.md` | **Branch**: `feat/F003-llm-routing`

### P0-F003-001 — Inference Pydantic models
**Depends on**: P0-F002-005 | **Est**: S | **Assigned**: cursor
**Goal**: Create `backend/app/models/inference.py`.
**Files allowed**: `backend/app/models/inference.py`, `backend/tests/unit/test_inference_models.py`

### P0-F003-002 — LLM router core
**Depends on**: P0-F002-005 | **Est**: M | **Assigned**: cursor
**Goal**: Create `backend/app/core/llm_router.py` LiteLLM wrapper with retry/fallback.
**Files allowed**: `backend/app/core/llm_router.py`, `backend/tests/unit/test_llm_router.py`

### P0-F003-003 — Rate limit service
**Depends on**: P0-F001-008 | **Est**: S | **Assigned**: cursor
**Goal**: Create `backend/app/services/rate_limit_service.py` Redis counters.
**Files allowed**: `backend/app/services/rate_limit_service.py`, `backend/tests/unit/test_rate_limit_service.py`

### P0-F003-004 — Inference service
**Depends on**: P0-F003-002, P0-F003-003 | **Est**: M | **Assigned**: cursor
**Goal**: Create `backend/app/services/inference_service.py`.
**Files allowed**: `backend/app/services/inference_service.py`, `backend/tests/unit/test_inference_service.py`

### P0-F003-005 — Inference API routes
**Depends on**: P0-F003-004 | **Est**: M | **Assigned**: cursor
**Goal**: Create `backend/app/api/inference.py` chat + stream endpoints.
**Files allowed**: `backend/app/api/inference.py`, `backend/app/main.py`, `backend/tests/integration/test_inference_api.py`

---

## F004 — Session Management
**Spec**: `specs/phase-0/F004-session-management.spec.md` | **Branch**: `feat/F004-sessions`

### P0-F004-001 — Session repository
**Depends on**: P0-F008-002 | **Est**: M | **Assigned**: cursor
**Goal**: Create `backend/app/db/session_repository.py`.
**Files allowed**: `backend/app/db/session_repository.py`, `backend/tests/unit/test_session_repository.py`

### P0-F004-002 — Redis client
**Depends on**: P0-F001-008 | **Est**: S | **Assigned**: cursor
**Goal**: Create `backend/app/db/redis_client.py`.
**Files allowed**: `backend/app/db/redis_client.py`, `backend/tests/unit/test_redis_client.py`

### P0-F004-003 — Session service
**Depends on**: P0-F004-001, P0-F004-002 | **Est**: M | **Assigned**: cursor
**Goal**: Create `backend/app/services/session_service.py` create/TTL/touch.
**Files allowed**: `backend/app/services/session_service.py`, `backend/tests/unit/test_session_service.py`

### P0-F004-004 — Budget service
**Depends on**: P0-F004-003 | **Est**: M | **Assigned**: cursor
**Goal**: Create `backend/app/services/budget_service.py` ledger and hard stop.
**Files allowed**: `backend/app/services/budget_service.py`, `backend/tests/unit/test_budget_service.py`

### P0-F004-005 — Session API routes
**Depends on**: P0-F004-004 | **Est**: M | **Assigned**: cursor
**Goal**: Create `backend/app/api/sessions.py`.
**Files allowed**: `backend/app/api/sessions.py`, `backend/app/main.py`, `backend/tests/integration/test_sessions_api.py`

### P0-F004-006 — Wire budget into inference
**Depends on**: P0-F004-004, P0-F003-004 | **Est**: S | **Assigned**: cursor
**Goal**: Inference service decrements budget and raises `BudgetExceededError`.
**Files allowed**: `backend/app/services/inference_service.py`, `backend/tests/unit/test_inference_budget.py`

### P0-F004-007 — Frontend session store
**Depends on**: P0-F004-005 | **Est**: M | **Assigned**: cursor
**Goal**: Create Zustand session store and bootstrap hook.
**Files allowed**: `frontend/lib/stores/session-store.ts`, `frontend/hooks/use-session.ts`, `frontend/package.json`

---

## F005 — Basic Conversation Interface
**Spec**: `specs/phase-0/F005-conversation-ui.spec.md` | **Branch**: `feat/F005-conversation-ui`

### P0-F005-001 — Message repository
**Depends on**: P0-F008-002 | **Est**: S | **Assigned**: cursor
**Goal**: Create `backend/app/db/message_repository.py`.
**Files allowed**: `backend/app/db/message_repository.py`, `backend/tests/unit/test_message_repository.py`

### P0-F005-002 — Message service
**Depends on**: P0-F005-001, P0-F003-004 | **Est**: M | **Assigned**: cursor
**Goal**: Create `backend/app/services/message_service.py`.
**Files allowed**: `backend/app/services/message_service.py`, `backend/tests/unit/test_message_service.py`

### P0-F005-003 — Messages API routes
**Depends on**: P0-F005-002, P0-F004-005 | **Est**: M | **Assigned**: cursor
**Goal**: Create `backend/app/api/messages.py` with stream/regenerate/clear.
**Files allowed**: `backend/app/api/messages.py`, `backend/tests/integration/test_messages_api.py`

### P0-F005-004 — Chat API client (SSE)
**Depends on**: P0-F004-007 | **Est**: M | **Assigned**: cursor
**Goal**: Create `frontend/lib/api/chat-client.ts` SSE consumer.
**Files allowed**: `frontend/lib/api/chat-client.ts`

### P0-F005-005 — Chat UI components
**Depends on**: P0-F005-004 | **Est**: L → split | **Assigned**: cursor
**Goal**: Create chat-container, message-list, message-bubble, chat-input components.
**Files allowed**: `frontend/components/chat/chat-container.tsx`, `message-list.tsx`, `message-bubble.tsx`, `chat-input.tsx`

### P0-F005-006 — Markdown renderer
**Depends on**: P0-F005-005 | **Est**: S | **Assigned**: cursor
**Goal**: Create safe `markdown-content.tsx` with react-markdown.
**Files allowed**: `frontend/components/chat/markdown-content.tsx`, `frontend/package.json`

### P0-F005-007 — Budget bar + chat page wiring
**Depends on**: P0-F005-005, P0-F004-007 | **Est**: M | **Assigned**: cursor
**Goal**: Wire `frontend/app/page.tsx`, budget-bar, use-chat hook.
**Files allowed**: `frontend/app/page.tsx`, `frontend/components/chat/budget-bar.tsx`, `frontend/hooks/use-chat.ts`

---

## F007 — Basic RAG Foundation
**Spec**: `specs/phase-0/F007-rag-foundation.spec.md` | **Branch**: `feat/F007-rag`

### P0-F007-001 — Document repository
**Depends on**: P0-F008-004 | **Est**: M | **Assigned**: cursor
**Goal**: Create `backend/app/db/document_repository.py`.
**Files allowed**: `backend/app/db/document_repository.py`, `backend/tests/unit/test_document_repository.py`

### P0-F007-002 — Chunking service
**Depends on**: none | **Est**: S | **Assigned**: cursor
**Goal**: Create `backend/app/services/chunking_service.py` RecursiveCharacterTextSplitter.
**Files allowed**: `backend/app/services/chunking_service.py`, `backend/tests/unit/test_chunking_service.py`

### P0-F007-003 — Embedding service
**Depends on**: P0-F003-002 | **Est**: M | **Assigned**: cursor
**Goal**: Create `backend/app/services/embedding_service.py` via LiteLLM.
**Files allowed**: `backend/app/services/embedding_service.py`, `backend/tests/unit/test_embedding_service.py`

### P0-F007-004 — RAG service
**Depends on**: P0-F007-001, P0-F007-002, P0-F007-003 | **Est**: M | **Assigned**: cursor
**Goal**: Create `backend/app/services/rag_service.py` ingest + retrieve.
**Files allowed**: `backend/app/services/rag_service.py`, `backend/tests/unit/test_rag_service.py`

### P0-F007-005 — Admin documents API
**Depends on**: P0-F007-004, P0-F006-001 | **Est**: M | **Assigned**: cursor
**Goal**: Create `backend/app/api/admin_documents.py`.
**Files allowed**: `backend/app/api/admin_documents.py`, `backend/tests/integration/test_admin_documents_api.py`

### P0-F007-006 — RAG inference integration
**Depends on**: P0-F007-004, P0-F003-004 | **Est**: S | **Assigned**: cursor
**Goal**: Inject retrieved chunks into inference system prompt when enabled.
**Files allowed**: `backend/app/services/inference_service.py`, `backend/tests/unit/test_inference_rag.py`

### P0-F007-007 — Admin documents UI
**Depends on**: P0-F007-005, P0-F006-005 | **Est**: M | **Assigned**: cursor
**Goal**: Create `frontend/app/admin/documents/page.tsx`.
**Files allowed**: `frontend/app/admin/documents/page.tsx`

---

## Phase 0 — Deferred / Human

| ID | Task | When |
|----|------|------|
| HT-009 | Verify `make dev` smoke | After P0-F001-008 |
| HT-008+ | Manual Phase 0 demo | After P0-F005-007 |
