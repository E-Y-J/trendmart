import json
from typing import List, Dict, Any, Optional

# Langchain imports
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

from .product_vector_store import ProductVectorStore
SYSTEM_PROMPT = (
    "You are a product recommendation assistant. Recommend items only from the provided context. "
    "If the context does not include directly relevant items, suggest related product categories "
    "that the user might search for next (e.g., supplements, gym gear). "
    "Do not invent specific product names not present in the context."
)


def _load_vs() -> ProductVectorStore:
    from .rag_service import load_simple_index
    return load_simple_index()


def _retrieve_products(question: str, k: int = 3) -> List[Dict[str, Any]]:
    vs = _load_vs()
    pairs = vs.search_similar_products(question, k=k)
    # Return just the product dicts from (product, score) pairs
    return [p for p, _score in pairs]
