# =============================================================================
# forge / app / constants
# =============================================================================
# Description : Application-wide constant values and environment file names.
# Layer       : Infra
# Feature     : F001 — Project Scaffolding
# Author      : cursor + KSR (reviewed by)
# Created     : 2026-06-17
# Modified    : 2026-06-17
# Version     : 0.1.0
# =============================================================================

ENV_LOCAL_FILENAME = ".env.local"
ENV_EXAMPLE_FILENAME = ".env.example"
DEFAULT_ENVIRONMENT = "development"

# LLM routing (F003)
DEFAULT_MODEL_ALIAS = "fast"
LLM_MAX_RETRIES = 3
LLM_RETRY_BASE_DELAY_SECONDS = 0.5
LLM_FALLBACK_ALIASES = ("fast", "smart", "cheap")

# OpenRouter free-tier models (no cost; good for local dev)
# See https://openrouter.ai/models?q=free — IDs change; verify periodically.
OPENROUTER_FREE_FAST_MODEL = "openrouter/free"
OPENROUTER_FREE_SMART_MODEL = "meta-llama/llama-3.3-70b-instruct:free"
OPENROUTER_FREE_CHEAP_MODEL = "mistralai/mistral-small-3.1-24b-instruct:free"
OPENROUTER_PROVIDER_PREFIX = "openrouter"

# Sessions (F004)
DEFAULT_SESSION_BUDGET_USD = 0.10
DEFAULT_SESSION_TTL_SECONDS = 7200
DEFAULT_MODEL_FOR_SESSION = "fast"

# API
CORRELATION_ID_HEADER = "X-Correlation-ID"
