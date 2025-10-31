import os
import json
import logging
from typing import List, Dict, Any, Optional

from .product_vector_store import ProductVectorStore
from .langchain_ollama import OllamaWrapper
from . import generator

logger = logging.getLogger(__name__)


INDEX_PATH = os.environ.get(
    "FAISS_INDEX_PATH", "./instance/product_index.json")


def load_simple_index():
    """Load the simple JSON index produced by index_products.py if present.

    Returns a ProductVectorStore instance with the products already added (in-memory).
    """
    if not os.path.exists(INDEX_PATH):
        # No index file; create an empty store
        return ProductVectorStore()

    with open(INDEX_PATH, "r", encoding="utf-8") as fh:
        payload = json.load(fh)

    products = payload.get("products", [])
    vs = ProductVectorStore()
    # add_products expects product dicts
    vs.add_products(products)
    return vs


def _ollama_llm_caller_factory(model: Optional[str] = None, temperature: float = 0.0):
    wrapper = OllamaWrapper(model=model, temperature=temperature)

    def _caller(messages: List[Dict[str, str]], *, model: Optional[str] = None, timeout: int = 30, temperature: float = 0.0) -> Dict[str, Any]:
        # Build a single prompt string from messages similar to generator.call_llm
        prompt = "\n\n".join(
            [f"{m.get('role').upper()}: {m.get('content')}" for m in messages])
        resp = wrapper.generate(prompt)
        # Ensure returned shape matches generator expectations
        return {"text": resp.get("text") if isinstance(resp, dict) else str(resp), "raw": resp.get("raw") if isinstance(resp, dict) else resp}

    return _caller


def answer_question(question: str, k: int = 5, temperature: float = 0.0, model: Optional[str] = None) -> Dict[str, Any]:
    """Answer a question using the simple RAG flow.

    This function prefers to use the simple JSON index (created by index_products.py)
    and the OllamaWrapper via an adapter that matches the `generator.generate_answer` contract.
    """
    # Load a product vector store (simple JSON-based index)
    vs = load_simple_index()

    # Retrieve top-k products using the product_vector_store's search
    retrieved = vs.search_similar_products(question, top_k=k)
    # Convert retrieved products into the context shape expected by generator.generate_answer
    context = []
    for prod, score in retrieved:
        # Expect prod to be a dict (indexer saved dicts)
        context.append(prod if isinstance(prod, dict) else prod)

    # Build an Ollama-based llm_caller and use generator.generate_answer for parsing and fail-closed behaviour
    llm_caller = _ollama_llm_caller_factory(
        model=model, temperature=temperature)

    res = generator.generate_answer(prompt=question, context=context,
                                    k=k, temperature=temperature, model=model, llm_caller=llm_caller)

    # attach retrieved metadata as raw sources if helpful
    res["_retrieved"] = [
        {"id": p.get("id"), "score": float(s)} for p, s in retrieved]
    return res
