# =============================================================================
# forge / app / services / chunking_service
# =============================================================================
# Description : Split document text into overlapping chunks for RAG embedding.
# Layer       : Core
# Feature     : F007 — Basic RAG Foundation
# Author      : cursor + KSR (reviewed by)
# Created     : 2026-06-17
# Modified    : 2026-06-17
# Version     : 0.1.0
# =============================================================================

from langchain_text_splitters import RecursiveCharacterTextSplitter

DEFAULT_CHUNK_SIZE = 512
DEFAULT_CHUNK_OVERLAP = 64


class ChunkingService:
    """Split plain text into sized chunks with configurable overlap."""

    def __init__(
        self,
        chunk_size: int = DEFAULT_CHUNK_SIZE,
        chunk_overlap: int = DEFAULT_CHUNK_OVERLAP,
    ) -> None:
        """
        Configure the recursive character text splitter.

        Args:
            chunk_size: Maximum characters per chunk.
            chunk_overlap: Overlap between consecutive chunks.

        Raises:
            ValueError: If overlap is not smaller than chunk size.
        """
        if chunk_overlap >= chunk_size:
            msg = "chunk_overlap must be less than chunk_size"
            raise ValueError(msg)
        self._splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            is_separator_regex=False,
        )

    def split_text(self, text: str) -> list[str]:
        """
        Split document text into chunks.

        Args:
            text: Raw document content.

        Returns:
            list[str]: Non-empty chunk strings in document order.

        Example:
            >>> ChunkingService(chunk_size=50).split_text("hello world")
            ['hello world']

        Notes:
            - Whitespace-only input returns an empty list.
            - See: specs/phase-0/F007-rag-foundation.spec.md
        """
        normalized = text.strip()
        if not normalized:
            return []
        chunks: list[str] = self._splitter.split_text(normalized)
        return chunks
