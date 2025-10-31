import os
import logging
from typing import List, Sequence, Union


TextLike = Union[str, Sequence[str]]


class BaseEmbeddingBackend:
    """Minimal embedding backend interface."""

    def embed(self, inputs: TextLike) -> Union[List[float], List[List[float]]]:
        raise NotImplementedError


class SentenceTransformersBackend(BaseEmbeddingBackend):
    def __init__(self, model_name: str | None = None):
        from sentence_transformers import SentenceTransformer  # lazy import

        self.model_name = (
            model_name
            or os.environ.get("HUGGINGFACE_EMBEDDING_MODEL")
            or "sentence-transformers/all-MiniLM-L6-v2"
        )
        self._model = SentenceTransformer(self.model_name)

    def embed(self, inputs: TextLike):
        # returns list(s)
        return self._model.encode(inputs, convert_to_tensor=False)


class OllamaEmbedBackend(BaseEmbeddingBackend):
    def __init__(self, model_name: str | None = None):
        self.model_name = (
            model_name
            or os.environ.get("OLLAMA_EMBED_MODEL")
            or "hf.co/CompendiumLabs/bge-base-en-v1.5-gguf"
        )

    def embed(self, inputs: TextLike):
        # Ensure inputs is a list for batch
        batched = inputs if isinstance(inputs, (list, tuple)) else [inputs]
        try:
            import ollama
        except Exception as exc:
            raise RuntimeError(
                "ollama python client not installed for embeddings") from exc

        out = ollama.embed(model=self.model_name, input=list(batched))
        # API returns dict with key 'embeddings': List[List[float]]
        vectors = out.get("embeddings") if isinstance(out, dict) else None
        if vectors is None:
            # Fallback: return as-is
            vectors = out
        if isinstance(inputs, (list, tuple)):
            return vectors
        # single input: return single vector
        return vectors[0] if vectors else []


logger = logging.getLogger(__name__)


def make_backend() -> BaseEmbeddingBackend:
    """Factory: choose Ollama embed if explicitly requested, else SentenceTransformers.

    If sentence-transformers is unavailable, automatically fall back to Ollama embed
    when possible, and otherwise raise a helpful error.
    """
    prefer_ollama = os.environ.get("USE_OLLAMA_EMBED") in {"1", "true", "True"} or bool(
        os.environ.get("OLLAMA_EMBED_MODEL")
    )
    if prefer_ollama:
        return OllamaEmbedBackend()

    # Try sentence-transformers first
    try:
        return SentenceTransformersBackend()
    except Exception as exc:
        logger.warning(
            "sentence-transformers not available, attempting Ollama embed fallback", exc_info=True
        )
        try:
            return OllamaEmbedBackend()
        except Exception:
            raise RuntimeError(
                "No embedding backend available. Install sentence-transformers or set USE_OLLAMA_EMBED=1 and have Ollama set up."
            ) from exc
