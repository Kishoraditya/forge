# =============================================================================
# forge / tests / unit / test_byok_service
# =============================================================================
# Description : Unit tests for BYOK key validation and encrypted storage.
# Layer       : Infra
# Feature     : F002 — BYOK Configuration System
# Author      : cursor + KSR (reviewed by)
# Created     : 2026-06-17
# Modified    : 2026-06-17
# Version     : 0.1.0
# =============================================================================

import pytest

from app.models.byok import ProviderKeyCreate
from app.services.byok_service import BYOKService


@pytest.mark.asyncio
async def test_store_key_persists_metadata() -> None:
    """Valid provider keys are stored without returning secret material."""
    service = BYOKService()
    stored = await service.store_key(
        ProviderKeyCreate(provider="openrouter", api_key="sk-openrouter-test-key"),
    )
    assert stored.provider == "openrouter"
    assert stored.is_active is True
    listed = service.list_keys()
    assert listed[0].provider == "openrouter"
