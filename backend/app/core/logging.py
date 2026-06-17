# =============================================================================
# forge / app / core / logging
# =============================================================================
# Description : Structlog configuration for structured application logging.
# Layer       : Core
# Feature     : F001 — Project Scaffolding
# Author      : cursor + KSR (reviewed by)
# Created     : 2026-06-17
# Modified    : 2026-06-17
# Version     : 0.1.0
# =============================================================================

import logging
import sys

import structlog

from app.config import get_settings


def configure_logging() -> None:
    """
    Configure structlog and stdlib logging per docs/LOGGING.md.

    Notes:
        - JSON in production; console renderer in development.
    """
    settings = get_settings()
    log_level = logging.DEBUG if settings.debug else logging.INFO
    logging.basicConfig(format="%(message)s", stream=sys.stdout, level=log_level)
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            (
                structlog.dev.ConsoleRenderer()
                if settings.debug
                else structlog.processors.JSONRenderer()
            ),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(log_level),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )
