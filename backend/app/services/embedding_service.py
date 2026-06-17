# =============================================================================
# forge / app / services / embedding_service
# =============================================================================
# Description : Generate text embeddings via LiteLLM for RAG retrieval.
# Layer       : Core
# Feature     : F007 — Basic RAG Foundation
# Author      : cursor + KSR (reviewed by)
# Created     : 2026-06-17
# Modified    : 2026-06-17
# Version     : 0.1.0
# =============================================================================

import litellm

from app.constants import DEFAULT_EMBEDDING_DIMENSIONS, DEFAULT_EMBEDDING_MODEL
from app.core.exceptions import AppValidationError


class EmbeddingService:
    """Create embedding vectors for document chunks and queries."""

    def __init__(self, model: str = DEFAULT_EMBEDDING_MODEL) -> None:
        """
        Initialize embedding service.

        Args:
            model: LiteLLM embedding model identifier.
        """
        self._model = model

    async def embed_texts(self, texts: list[str]) -> list[list[float]]:
        """
        Embed multiple text strings.

        Args:
            texts: Non-empty list of strings to embed.

        Returns:
            list[list[float]]: Embedding vectors aligned with input order.

        Raises:
            AppValidationError: When texts is empty or embedding fails.
        """
        if not texts:
            msg = "No texts to embed"
            raise AppValidationError(msg)
        try:
            response = await litellm.aembedding(model=self._model, input=texts)
        except Exception as exc:
            msg = f"Embedding failed: {exc}"
            raise AppValidationError(msg) from exc
        data = response.data
        vectors: list[list[float]] = []
        for item in data:
            embedding = (
                item.get("embedding")
                if isinstance(item, dict)
                else getattr(item, "embedding", None)
            )
            if embedding is None:
                msg = "Embedding response missing vector"
                raise AppValidationError(msg)
            vectors.append(list(embedding))
        return vectors

    async def embed_query(self, query: str) -> list[float]:
        """
        Embed a single query string.

        Args:
            query: Search query text.

        Returns:
            list[float]: Query embedding vector.
        """
        vectors = await self.embed_texts([query])
        return vectors[0]

    @property
    def dimensions(self) -> int:
        """Return expected embedding vector size."""
        return DEFAULT_EMBEDDING_DIMENSIONS
