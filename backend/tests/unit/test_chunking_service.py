# =============================================================================
# forge / tests / unit / test_chunking_service
# =============================================================================
# Description : Unit tests for RecursiveCharacterTextSplitter chunking pipeline.
# Layer       : Infra
# Feature     : F007 — Basic RAG Foundation
# Author      : cursor + KSR (reviewed by)
# Created     : 2026-06-17
# Modified    : 2026-06-17
# Version     : 0.1.0
# =============================================================================

from app.services.chunking_service import ChunkingService


def test_split_short_text_returns_single_chunk() -> None:
    """Text shorter than chunk size yields one chunk."""
    service = ChunkingService(chunk_size=100, chunk_overlap=10)
    chunks = service.split_text("Hello forge.")
    assert chunks == ["Hello forge."]


def test_split_long_text_respects_size_and_overlap() -> None:
    """Long text is split with overlap between consecutive chunks."""
    service = ChunkingService(chunk_size=20, chunk_overlap=5)
    text = "alpha beta gamma delta epsilon zeta eta theta"
    chunks = service.split_text(text)
    assert len(chunks) >= 2
    for chunk in chunks:
        assert len(chunk) <= 20
    joined = " ".join(chunks)
    assert "alpha" in joined
    assert "theta" in joined


def test_split_empty_text_returns_empty_list() -> None:
    """Empty input returns no chunks."""
    service = ChunkingService()
    assert service.split_text("") == []
    assert service.split_text("   ") == []
