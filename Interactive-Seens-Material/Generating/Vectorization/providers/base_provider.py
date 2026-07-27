"""
Base Embedding Provider — Abstract interface for embedding generation.

All embedding providers must implement this interface.
The VectorizationManager depends ONLY on this abstraction.
"""

import logging
from abc import ABC, abstractmethod
from typing import Optional

logger = logging.getLogger(__name__)


class EmbeddingProvider(ABC):
    """
    Abstract embedding provider interface.

    Concrete implementations:
        - GeminiProvider (Google Generative AI)
        - Future: SentenceTransformersProvider, OpenAIProvider,
          BAAIProvider, NomicProvider, etc.

    Usage:
        provider = GeminiProvider(model="models/text-embedding-004")
        vector = provider.embed("Hello world")
        vectors = provider.embed_batch(["Hello", "World"])
    """

    @property
    @abstractmethod
    def model_name(self) -> str:
        """Return the model identifier string."""
        ...

    @property
    @abstractmethod
    def dimension(self) -> int:
        """Return the output vector dimensionality."""
        ...

    @abstractmethod
    def embed(self, text: str) -> list[float]:
        """
        Generate an embedding vector for a single text string.

        Args:
            text: The input text to embed.

        Returns:
            A list of floats representing the embedding vector.

        Raises:
            EmbeddingError: If embedding generation fails.
        """
        ...

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """
        Generate embeddings for multiple texts.

        Default implementation calls embed() sequentially.
        Providers may override with batch-optimized implementations.

        Args:
            texts: List of input texts.

        Returns:
            List of embedding vectors (same order as input).
        """
        logger.info(f"Embedding batch of {len(texts)} texts (sequential)")
        return [self.embed(text) for text in texts]


class EmbeddingError(Exception):
    """Raised when an embedding generation call fails."""
    pass
