"""
Gemini Embedding Provider — Google Generative AI embeddings.

Uses google.generativeai.embed_content() to generate embeddings.
Requires the google-generativeai package (already a project dependency).
"""

import logging
from typing import Optional

from Generating.Vectorization.providers.base_provider import (
    EmbeddingError,
    EmbeddingProvider,
)
from Generating.config import (
    AI_API_KEY,
    EMBEDDING_DIMENSION,
    EMBEDDING_MODEL,
    EMBEDDING_TASK_TYPE,
)

logger = logging.getLogger(__name__)


class GeminiProvider(EmbeddingProvider):
    """
    Embedding provider using Google Generative AI.

    Usage:
        provider = GeminiProvider()
        vector = provider.embed("Mitochondria is the powerhouse of the cell")
    """

    def __init__(
        self,
        model: Optional[str] = None,
        dimension: Optional[int] = None,
        task_type: Optional[str] = None,
        api_key: Optional[str] = None,
    ):
        self._model = model or EMBEDDING_MODEL
        self._dimension = dimension or EMBEDDING_DIMENSION
        self._task_type = task_type or EMBEDDING_TASK_TYPE
        self._api_key = api_key or AI_API_KEY

        self._initialized = False

    def _ensure_initialized(self) -> None:
        """Lazy-initialize the Gemini SDK."""
        if self._initialized:
            return
        try:
            import google.generativeai as genai
            genai.configure(api_key=self._api_key)
            self._genai = genai
            self._initialized = True
            logger.info(
                f"GeminiProvider initialized: model={self._model}, "
                f"dimension={self._dimension}"
            )
        except ImportError:
            raise EmbeddingError(
                "google-generativeai package not installed. "
                "Run: pip install google-generativeai"
            )

    @property
    def model_name(self) -> str:
        return self._model

    @property
    def dimension(self) -> int:
        return self._dimension

    def embed(self, text: str) -> list[float]:
        """Generate embedding using Gemini embed_content API."""
        self._ensure_initialized()
        try:
            result = self._genai.embed_content(
                model=self._model,
                content=text,
                task_type=self._task_type,
                output_dimensionality=self._dimension,
            )
            return result["embedding"]
        except Exception as e:
            raise EmbeddingError(
                f"Gemini embedding failed: {e}"
            ) from e

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """
        Batch embedding using Gemini.

        Gemini supports batch embedding natively via embed_content
        with a list of content strings.
        """
        self._ensure_initialized()
        try:
            vectors = []
            for text in texts:
                result = self._genai.embed_content(
                    model=self._model,
                    content=text,
                    task_type=self._task_type,
                    output_dimensionality=self._dimension,
                )
                vectors.append(result["embedding"])
            return vectors
        except Exception as e:
            raise EmbeddingError(
                f"Gemini batch embedding failed: {e}"
            ) from e
