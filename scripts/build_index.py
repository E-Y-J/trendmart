import os
import sys
import json
import argparse
from pathlib import Path
from typing import Iterable, Dict, Any, List, Tuple


def _find_repo_root(start: Path, marker: str = "backend", max_up: int = 6) -> Path:
    cur = start.resolve()
    for _ in range(max_up):
        if (cur / marker).is_dir():
            return cur
        if cur.parent == cur:
            break
        cur = cur.parent
    return start.resolve()


REPO_ROOT = _find_repo_root(Path(__file__).resolve().parent)
sys.path.insert(0, str(REPO_ROOT))  # so we can import backend.*


def _load_sample_products() -> Tuple[List[Dict[str, Any]], Dict[int, Dict[str, Any]]]:
    """Parse sample_data/product_data.js and return (products, category_info_by_id).

    The JS file exports a large JSON-like object. We'll extract the first JSON object
    and parse it with json.loads.
    """
    js_path = REPO_ROOT / "sample_data" / "product_data.js"
    if not js_path.exists():
        raise FileNotFoundError(f"Sample data not found at {js_path}")

    text = js_path.read_text(encoding="utf-8")
    # find first '{' and last '}' to isolate the JSON payload
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end <= start:
        raise ValueError(
            "Unable to parse sample_data/product_data.js: JSON braces not found")
    payload = json.loads(text[start:end + 1])

    products: List[Dict[str, Any]] = []
    cat_info: Dict[int, Dict[str, Any]] = {}

    for cat in payload.get("categories", []):
        main_cat = cat.get("main_category", "")
        for sub in cat.get("subcategories", []):
            sub_name = sub.get("name", "")
            for p in sub.get("products", []):
                # ensure required fields exist
                p = dict(p)
                p.setdefault("name", "")
                p.setdefault("tags", [])
                p.setdefault("price", 0)
                p.setdefault("rating", 0)
                products.append(p)
                pid = p.get("id")
                if pid is not None:
                    cat_info[int(pid)] = {
                        "main_category": main_cat, "subcategory": sub_name}

    return products, cat_info


def build_from_db():
    # Import here after sys.path modification
    from backend.app import create_app
    from backend.ai_recom_system.index_products import index_all_products

    app = create_app()
    with app.app_context():
        index_all_products()


def build_sample_index():
    from backend.ai_recom_system.index_products import index_all_products

    try:
        products, category_info = _load_sample_products()
    except Exception:
        # Fallback tiny sample if sample_data is missing
        products = [
            {"id": 1, "name": "Blue Sneakers", "description": "Comfortable running sneakers",
                "price": 79.99, "rating": 4.4, "tags": ["sneakers", "running"]},
            {"id": 2, "name": "Trail Boots", "description": "Waterproof trail boots",
                "price": 119.0, "rating": 4.5, "tags": ["boots", "trail"]},
        ]
        category_info = {}

    def fetch_products() -> Iterable[Dict[str, Any]]:
        # Enrich products with category metadata if available
        enriched: List[Dict[str, Any]] = []
        for p in products:
            q = dict(p)
            pid = q.get("id")
            if pid is not None and int(pid) in category_info:
                info = category_info[int(pid)]
                q.setdefault("category_info", info)
                q.setdefault("main_category", info.get("main_category"))
                q.setdefault("subcategory", info.get("subcategory"))
            enriched.append(q)
        return enriched

    index_all_products(fetch_products_fn=fetch_products)


def main(argv: List[str] | None = None):
    p = argparse.ArgumentParser(description="Build product vector index")
    p.add_argument('--sample', action='store_true',
                   help='Build a sample index from sample_data')
    args = p.parse_args(argv)

    if args.sample:
        print("Building sample product index...")
        build_sample_index()
    else:
        print("Building product index from database...")
        build_from_db()
    print('Done.')


if __name__ == '__main__':
    main()
