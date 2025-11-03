"""Hugging Face embeddings adapter with a sentence-transformers fallback.

This module provides HFEmbeddingClient which prefers the Hugging Face
Inference API when an API key is provided. If no
API key is available, it falls back to a local sentence-transformers model
if installed.

Usage:
    client = HFEmbeddingClient(api_key=os.environ.get('HUGGINGFACE_API_KEY'), model='compendium/bge')
    vectors = client.embed(["text1", "text2"])
"""
from typing import List, Optional
import os
import logging

logger = logging.getLogger(__name__)


class HFEmbeddingClient:
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        """Create an embeddings client.

        If api_key is provided we will use huggingface_hub.InferenceClient.
        Otherwise we attempt to use sentence-transformers locally.
        """
        self.api_key = api_key or os.environ.get("HUGGINGFACE_API_KEY")
        # sensible default embedding model (can be overridden by env or caller)
        self.model = model or os.environ.get("EMBED_MODEL", "all-MiniLM-L6-v2")

        self._hf_client = None
        self._local_model = None

    def _init_hf(self):
        try:
            from huggingface_hub import InferenceClient

            self._hf_client = InferenceClient(token=self.api_key)
            logger.debug("Using Hugging Face InferenceClient for embeddings")
        except Exception as exc:  # pragma: no cover - external
            logger.debug("Hugging Face InferenceClient not available: %s", exc)
            self._hf_client = None

    def _init_local(self):
        try:
            from sentence_transformers import SentenceTransformer

            self._local_model = SentenceTransformer(self.model)
            logger.debug(
                "Using local SentenceTransformer model: %s", self.model)
        except Exception as exc:  # pragma: no cover - optional
            logger.debug("Local SentenceTransformer not available: %s", exc)
            self._local_model = None

    def embed(self, texts: List[str]) -> List[List[float]]:
        """Return embedding vectors for the provided texts.

        This method is intentionally tolerant: it will try the HF Inference API
        (if api_key is set), then fall back to a local sentence-transformers
        model if available. It raises RuntimeError only if no method is
        available.
        """
        if not texts:
            return []

        # Try HF Inference API first when API key is set
        if self.api_key:
            if self._hf_client is None:
                self._init_hf()
            if self._hf_client is not None:
                try:
                    # InferenceClient may expose different convenviences across versions.
                    # Try the common embed/embeddings entry points, falling back as needed.
                    if hasattr(self._hf_client, "embed"):
                        resp = self._hf_client.embed(
                            model=self.model, input=texts)
                        # response shape may vary: try to normalize
                        if isinstance(resp, dict) and "embeddings" in resp:
                            return resp["embeddings"]
                        return resp
                    if hasattr(self._hf_client, "embeddings"):
                        resp = self._hf_client.embeddings(
                            model=self.model, inputs=texts)
                        # normalization
                        if isinstance(resp, dict) and "embeddings" in resp:
                            return resp["embeddings"]
                        return resp
                    # last resort: call inference endpoint and try to parse
                    out = self._hf_client(inputs=texts, model=self.model)
                    if isinstance(out, dict) and "embeddings" in out:
                        return out["embeddings"]
                except Exception as exc:  # pragma: no cover - network
                    logger.warning("Hugging Face embed call failed: %s", exc)

        # Fallback to local sentence-transformers
        if self._local_model is None:
            self._init_local()
        if self._local_model is not None:
            vectors = self._local_model.encode(texts, show_progress_bar=False)
            # ensure Python list of lists
            return [list(map(float, v)) for v in vectors]

        raise RuntimeError(
            "No embeddings backend available (provide HUGGINGFACE_API_KEY or install sentence-transformers)")
