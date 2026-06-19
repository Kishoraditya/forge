# =============================================================================
# forge / tests / unit / test_rag_service
# =============================================================================
# Description : Unit tests for document ingestion and retrieval orchestration.
# Layer       : Infra
# Feature     : F007 — Basic RAG Foundation
# Author      : cursor + KSR (reviewed by)
# Created     : 2026-06-17
# Modified    : 2026-06-17
# Version     : 0.1.0
# =============================================================================

import pytest

from app.services.rag_service import RAGService


@pytest.mark.asyncio
async def test_ingest_and_retrieve_text_document() -> None:
    """TXT upload is chunked, embedded, and retrievable."""
    service = RAGService()
    await service.ingest_document(
        "forge.txt",
        "text/plain",
        b"Forge is a BYOK agent workbench for multi-session workflows.",
    )
    result = await service.retrieve("What is Forge?", top_k=1)
    assert result.chunks
    assert result.scores[0] > 0
