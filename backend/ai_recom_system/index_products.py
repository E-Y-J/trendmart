import os
import json
from typing import List

from .product_vector_store import ProductVectorStore

# Path to save a simple persisted index (numpy/JSON via the ProductVectorStore is used)
INDEX_PATH = os.environ.get(
    "FAISS_INDEX_PATH", "./instance/product_index.json")


def index_all_products(fetch_products_fn=None):
    """Index products by loading them from the application DB and saving a simple index file.

    Args:
        fetch_products_fn: optional function that returns iterable of product dicts. If not
                           provided, this function will attempt to import models and query the DB
                           (requires app context).
    """
    # Fetch product dicts
    if fetch_products_fn is None:
        # Lazy import to avoid app context issues at module import time
        try:
            from models.catalog import Product
            # Attempt to query ORM if available
            prods = [p.to_dict() for p in Product.query.all()]
        except Exception:
            raise RuntimeError(
                "Provide fetch_products_fn when running outside app context")
    else:
        prods = list(fetch_products_fn())

    if not prods:
        print("No products found to index")
        return

    # Use the existing ProductVectorStore to compute embeddings
    vs = ProductVectorStore()
    vs.add_products(prods)

    # Persist products and embeddings for reuse by the simple RAG fallback
    out = {
        "products": vs.products,
        "embeddings": vs.product_embeddings,
        "embedding_dimension": len(vs.product_embeddings[0]) if vs.product_embeddings else 0,
        "embeddings_count": len(vs.product_embeddings)
    }
    os.makedirs(os.path.dirname(INDEX_PATH), exist_ok=True)
    with open(INDEX_PATH, "w", encoding="utf-8") as fh:
        json.dump(out, fh, default=str)

    print(f"Saved simple product index to {INDEX_PATH}")


if __name__ == "__main__":
    index_all_products()
