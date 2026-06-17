# =============================================================================
# forge / app / config
# =============================================================================
# Description : Pydantic Settings loading validated configuration from environment.
# Layer       : Infra
# Feature     : F001 — Project Scaffolding
# Author      : cursor + KSR (reviewed by)
# Created     : 2026-06-17
# Modified    : 2026-06-17
# Version     : 0.1.0
# =============================================================================

from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.constants import DEFAULT_ENVIRONMENT, ENV_LOCAL_FILENAME

PROJECT_ROOT = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables and `.env.local`.

    Secrets are never logged. See specs/phase-0/F001-scaffolding.spec.md.
    """

    environment: str = Field(default=DEFAULT_ENVIRONMENT)
    debug: bool = Field(default=False)
    redis_url: str
    neo4j_uri: str
    neo4j_username: str
    neo4j_password: str
    supabase_url: str
    supabase_anon_key: str
    supabase_service_role_key: str
    supabase_jwt_secret: str | None = Field(default=None)
    admin_email: str | None = Field(default=None)
    anthropic_api_key: str | None = Field(default=None)
    openrouter_api_key: str | None = Field(default=None)
    default_session_budget_usd: float = Field(default=0.10)
    session_ttl_seconds: int = Field(default=7200)
    default_model_alias: str = Field(default="fast")
    cors_origins: str = Field(default="http://localhost:3000")

    @property
    def cors_origin_list(self) -> list[str]:
        """Parse comma-separated CORS origins."""
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]

    model_config = SettingsConfigDict(
        env_file=(PROJECT_ROOT / ENV_LOCAL_FILENAME, PROJECT_ROOT / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )


@lru_cache
def get_settings() -> Settings:
    """
    Return cached application settings singleton.

    Returns:
        Settings: Validated settings instance.

    Example:
        >>> settings = get_settings()
        >>> settings.environment
        'development'

    Notes:
        - Cache clears only on process restart.
        - See: specs/phase-0/F001-scaffolding.spec.md
    """
    return Settings()


def reset_settings_cache() -> None:
    """
    Clear the settings cache (for tests only).

    Notes:
        - Do not use in production code paths.
    """
    get_settings.cache_clear()
