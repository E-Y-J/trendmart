from __future__ import annotations

from dataclasses import dataclass
from typing import List, Dict, Any, Optional

from .product_vector_store import ProductVectorStore


@dataclass
class Document:
    page_content: str
    metadata: Dict[str, Any]


class SimpleProductRetriever:
    """Minimal retriever adapter that mimics LangChain's retriever returning Documents."""

    def __init__(self, store: Optional[ProductVectorStore] = None):
        self.store = store or ProductVectorStore()

    def _to_doc(self, product: Dict[str, Any], score: float) -> Document:
        content = f"{product.get('name','')}. {product.get('description','')}"
        meta = {
            "id": product.get("id"),
            "name": product.get("name"),
            "score": float(score),
        }
        return Document(page_content=content, metadata=meta)

    def get_relevant_documents(self, query: str, k: int = 5) -> List[Document]:
        results = self.store.search_similar_products(query, top_k=k)
        return [self._to_doc(prod, score) for prod, score in results]
