# =============================================================================
# forge / app / services / rag_service
# =============================================================================
# Description : Ingest documents and retrieve top-k chunks for RAG context.
# Layer       : Core
# Feature     : F007 — Basic RAG Foundation
# Author      : cursor + KSR (reviewed by)
# Created     : 2026-06-17
# Modified    : 2026-06-17
# Version     : 0.1.0
# =============================================================================

import io
from uuid import UUID, uuid4

from pypdf import PdfReader

from app.constants import ALLOWED_UPLOAD_MIME_TYPES, DEFAULT_RAG_TOP_K, MAX_UPLOAD_BYTES
from app.core.exceptions import AppValidationError, NotFoundError
from app.db.document_repository import DocumentRepository
from app.db.memory_store import DocumentChunkRow
from app.models.document import DocumentRecord, RetrievalResult
from app.services.chunking_service import ChunkingService
from app.services.embedding_service import EmbeddingService


class RAGService:
    """Document ingestion and semantic retrieval orchestration."""

    def __init__(
        self,
        documents: DocumentRepository | None = None,
        chunking: ChunkingService | None = None,
        embeddings: EmbeddingService | None = None,
    ) -> None:
        """
        Initialize RAG service dependencies.

        Args:
            documents: Document repository.
            chunking: Text chunking service.
            embeddings: Embedding service.
        """
        self._documents = documents or DocumentRepository()
        self._chunking = chunking or ChunkingService()
        self._embeddings = embeddings or EmbeddingService()

    def _extract_text(self, filename: str, mime_type: str, raw: bytes) -> str:
        """
        Extract plain text from uploaded bytes.

        Args:
            filename: Original filename.
            mime_type: MIME type.
            raw: File bytes.

        Returns:
            str: Extracted text content.

        Raises:
            AppValidationError: When file is empty or unsupported.
        """
        if not raw.strip():
            msg = "Uploaded file is empty"
            raise AppValidationError(msg)
        if mime_type == "application/pdf":
            reader = PdfReader(io.BytesIO(raw))
            pages = [page.extract_text() or "" for page in reader.pages]
            text = "\n".join(pages).strip()
            if not text:
                msg = f"Could not extract text from PDF: {filename}"
                raise AppValidationError(msg)
            return text
        try:
            return raw.decode("utf-8").strip()
        except UnicodeDecodeError as exc:
            msg = f"Unsupported text encoding for {filename}"
            raise AppValidationError(msg) from exc

    async def ingest_document(self, filename: str, mime_type: str, raw: bytes) -> DocumentRecord:
        """
        Store, chunk, embed, and persist an uploaded document.

        Args:
            filename: Original filename.
            mime_type: MIME type.
            raw: File bytes.

        Returns:
            DocumentRecord: Created document metadata.
        """
        if mime_type not in ALLOWED_UPLOAD_MIME_TYPES:
            msg = f"Unsupported file type: {mime_type}"
            raise AppValidationError(msg)
        if len(raw) > MAX_UPLOAD_BYTES:
            msg = f"File exceeds {MAX_UPLOAD_BYTES} bytes"
            raise AppValidationError(msg)
        text = self._extract_text(filename, mime_type, raw)
        doc = self._documents.create_document(filename, mime_type, len(raw))
        parts = self._chunking.split_text(text)
        vectors = await self._embeddings.embed_texts(parts)
        chunks = [
            DocumentChunkRow(
                id=uuid4(),
                document_id=doc.id,
                content=part,
                embedding=vector,
                chunk_index=index,
            )
            for index, (part, vector) in enumerate(zip(parts, vectors, strict=True))
        ]
        self._documents.save_chunks(doc.id, chunks)
        return DocumentRecord(
            id=doc.id,
            filename=doc.filename,
            mime_type=doc.mime_type,
            size_bytes=doc.size_bytes,
            created_at=doc.created_at,
        )

    def list_documents(self) -> list[DocumentRecord]:
        """
        List uploaded documents.

        Returns:
            list[DocumentRecord]: Document metadata rows.
        """
        return [
            DocumentRecord(
                id=row.id,
                filename=row.filename,
                mime_type=row.mime_type,
                size_bytes=row.size_bytes,
                created_at=row.created_at,
            )
            for row in self._documents.list_documents()
        ]

    def delete_document(self, document_id: UUID) -> None:
        """
        Delete a document by ID.

        Args:
            document_id: Document UUID.

        Raises:
            NotFoundError: When document does not exist.
        """
        if not self._documents.delete_document(document_id):
            raise NotFoundError("Document not found")

    async def retrieve(self, query: str, top_k: int = DEFAULT_RAG_TOP_K) -> RetrievalResult:
        """
        Retrieve top-k relevant chunks for a query.

        Args:
            query: User query text.
            top_k: Maximum chunks to return.

        Returns:
            RetrievalResult: Chunk texts and similarity scores.
        """
        query_vector = await self._embeddings.embed_query(query)
        hits = self._documents.search_similar(query_vector, top_k)
        return RetrievalResult(
            chunks=[chunk.content for chunk, _score in hits],
            scores=[score for _chunk, score in hits],
        )
