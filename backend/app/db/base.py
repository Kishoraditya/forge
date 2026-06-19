# =============================================================================
# forge / app / db / base
# =============================================================================
# Description : SQLAlchemy declarative base for Phase 0 ORM models.
# Layer       : Memory
# Feature     : F008 — Supabase Schema Foundation
# Author      : cursor + KSR (reviewed by)
# Created     : 2026-06-17
# Modified    : 2026-06-17
# Version     : 0.1.0
# =============================================================================

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Declarative base for Forge SQLAlchemy models."""
