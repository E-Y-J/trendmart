"""Public API for the ai_recom_system package.

Keep this file minimal to avoid importing submodules that aren't meant to be
executed at package import time. Heavy modules (models, helpers) should be
imported by consumers explicitly or lazily inside functions.
"""

from .product_vector_store import ProductVectorStore

__all__ = ["ProductVectorStore"]
