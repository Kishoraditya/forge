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

# Sessions (F004)
DEFAULT_SESSION_BUDGET_USD = 0.10
DEFAULT_SESSION_TTL_SECONDS = 7200
DEFAULT_MODEL_FOR_SESSION = "fast"

# API
CORRELATION_ID_HEADER = "X-Correlation-ID"
