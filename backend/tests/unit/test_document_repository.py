# =============================================================================
# forge / tests / unit / test_document_repository
# =============================================================================
# Description : Unit tests for in-memory document repository and vector search.
# Layer       : Infra
# Feature     : F007 — Basic RAG Foundation
# Author      : cursor + KSR (reviewed by)
# Created     : 2026-06-17
# Modified    : 2026-06-17
# Version     : 0.1.0
# =============================================================================

from uuid import uuid4

from app.db.document_repository import DocumentRepository
from app.db.memory_store import DocumentChunkRow


def test_create_and_list_documents() -> None:
    """Documents can be created and listed."""
    repo = DocumentRepository()
    doc = repo.create_document("readme.md", "text/markdown", 128)
    listed = repo.list_documents()
    assert len(listed) == 1
    assert listed[0].id == doc.id


def test_search_similar_returns_top_match() -> None:
    """Cosine search returns highest-scoring chunk."""
    repo = DocumentRepository()
    doc = repo.create_document("notes.txt", "text/plain", 64)
    chunks = [
        DocumentChunkRow(
            id=uuid4(),
            document_id=doc.id,
            content="forge rag foundation",
            embedding=[1.0, 0.0, 0.0],
            chunk_index=0,
        ),
        DocumentChunkRow(
            id=uuid4(),
            document_id=doc.id,
            content="unrelated text",
            embedding=[0.0, 1.0, 0.0],
            chunk_index=1,
        ),
    ]
    repo.save_chunks(doc.id, chunks)
    hits = repo.search_similar([1.0, 0.0, 0.0], top_k=1)
    assert len(hits) == 1
    assert hits[0][0].content == "forge rag foundation"
