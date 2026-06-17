# =============================================================================
# forge / app / db / document_repository
# =============================================================================
# Description : Document and chunk persistence (memory; Postgres when configured).
# Layer       : Memory
# Feature     : F007 — Basic RAG Foundation
# Author      : cursor + KSR (reviewed by)
# Created     : 2026-06-17
# Modified    : 2026-06-17
# Version     : 0.1.0
# =============================================================================

import math
from datetime import UTC, datetime
from uuid import UUID, uuid4

from app.db.memory_store import DocumentChunkRow, DocumentRow, get_memory_store


def _cosine_similarity(left: list[float], right: list[float]) -> float:
    """
    Compute cosine similarity between two vectors.

    Args:
        left: First embedding vector.
        right: Second embedding vector.

    Returns:
        float: Similarity score in [-1, 1].
    """
    if len(left) != len(right):
        return -1.0
    dot = sum(a * b for a, b in zip(left, right, strict=True))
    left_norm = math.sqrt(sum(a * a for a in left))
    right_norm = math.sqrt(sum(b * b for b in right))
    if left_norm == 0 or right_norm == 0:
        return -1.0
    return dot / (left_norm * right_norm)


class DocumentRepository:
    """CRUD and vector search for uploaded documents."""

    def create_document(self, filename: str, mime_type: str, size_bytes: int) -> DocumentRow:
        """
        Insert document metadata.

        Args:
            filename: Original filename.
            mime_type: MIME type string.
            size_bytes: File size in bytes.

        Returns:
            DocumentRow: Created document row.
        """
        row = DocumentRow(
            id=uuid4(),
            filename=filename,
            mime_type=mime_type,
            size_bytes=size_bytes,
            created_at=datetime.now(UTC),
        )
        get_memory_store().documents[row.id] = row
        get_memory_store().document_chunks[row.id] = []
        return row

    def list_documents(self) -> list[DocumentRow]:
        """
        List all documents ordered by creation time descending.

        Returns:
            list[DocumentRow]: Stored documents.
        """
        rows = list(get_memory_store().documents.values())
        return sorted(rows, key=lambda row: row.created_at, reverse=True)

    def get_document(self, document_id: UUID) -> DocumentRow | None:
        """
        Fetch document by ID.

        Args:
            document_id: Document UUID.

        Returns:
            DocumentRow | None: Document if found.
        """
        return get_memory_store().documents.get(document_id)

    def delete_document(self, document_id: UUID) -> bool:
        """
        Delete document and associated chunks.

        Args:
            document_id: Document UUID.

        Returns:
            bool: True when document existed and was removed.
        """
        store = get_memory_store()
        if document_id not in store.documents:
            return False
        del store.documents[document_id]
        store.document_chunks.pop(document_id, None)
        return True

    def save_chunks(
        self,
        document_id: UUID,
        chunks: list[DocumentChunkRow],
    ) -> list[DocumentChunkRow]:
        """
        Replace chunks for a document.

        Args:
            document_id: Parent document UUID.
            chunks: Chunk rows to persist.

        Returns:
            list[DocumentChunkRow]: Saved chunks.
        """
        get_memory_store().document_chunks[document_id] = chunks
        return chunks

    def list_chunks(self, document_id: UUID) -> list[DocumentChunkRow]:
        """
        List chunks for a document.

        Args:
            document_id: Document UUID.

        Returns:
            list[DocumentChunkRow]: Ordered chunks.
        """
        chunks = get_memory_store().document_chunks.get(document_id, [])
        return sorted(chunks, key=lambda row: row.chunk_index)

    def search_similar(
        self,
        query_embedding: list[float],
        top_k: int,
    ) -> list[tuple[DocumentChunkRow, float]]:
        """
        Return top-k chunks by cosine similarity.

        Args:
            query_embedding: Query vector.
            top_k: Maximum results to return.

        Returns:
            list[tuple[DocumentChunkRow, float]]: Chunk and score pairs.
        """
        scored: list[tuple[DocumentChunkRow, float]] = []
        store = get_memory_store()
        for chunk_list in store.document_chunks.values():
            for chunk in chunk_list:
                if not chunk.embedding:
                    continue
                score = _cosine_similarity(query_embedding, chunk.embedding)
                scored.append((chunk, score))
        scored.sort(key=lambda item: item[1], reverse=True)
        return scored[:top_k]
