from flask import Blueprint, request, jsonify, current_app, make_response
from marshmallow import fields, ValidationError
from extensions import ValidationSchema
import threading
import os
import time
import uuid
from typing import List, Dict, Any, Optional, Tuple
from ai_recom_system.rag_service import answer_question, load_simple_index, INDEX_PATH

# Blueprint placed here to prevent circular imports
recom_bp = Blueprint('recommendation', __name__, url_prefix='/recommendations')

_vector_store = None  # Placeholder for vector store initialization
_vector_lock = threading.Lock()
_vs_cache = None  # type: Optional[object]
_vs_cache_mtime = None  # type: Optional[float]


def _init_vector_store():
    '''Initialize the ProductVectorStore from app config.'''
    from ai_recom_system.product_vector_store import ProductVectorStore

    model_name = current_app.config.get('EMBED_MODEL', 'all-MiniLM-L6-v2')
    vs = ProductVectorStore(model_name=model_name)
    return vs


def _now_ms() -> int:
    '''Return current time in milliseconds.'''
    return int(time.time() * 1000)


def _req_id() -> str:
    '''Generate a short unique request ID.'''
    return uuid.uuid4().hex[:12]


def _json_response(payload: Dict[str, Any], status: int = 200, req_id: Optional[str] = None):
    '''Helper to create a JSON response with optional request ID header.'''
    resp = make_response(jsonify(payload), status)
    if req_id:
        resp.headers['X-Request-ID'] = req_id
    return resp


def _get_vs_cached() -> Tuple[object, Dict[str, Any]]:
    """Return a cached ProductVectorStore, reloading only if the index file changed."""
    global _vs_cache, _vs_cache_mtime
    idx_path = INDEX_PATH
    mtime = None

    try:
        # Get the last modified time of the index file
        mtime = os.path.getmtime(idx_path)
    except Exception:
        # Failed to get mtime; treat as not modified
        mtime = None

    with _vector_lock:
        # Reload if cache is empty or index file changed
        if _vs_cache is None or (_vs_cache_mtime is not None and mtime is not None and mtime > _vs_cache_mtime):
            _vs_cache = load_simple_index()
            _vs_cache_mtime = mtime

    stats = {}
    try:
        # Get stats from the vector store
        stats = _vs_cache.get_stats() if _vs_cache else {}
    except Exception:
        # Failed to get stats; treat as empty
        stats = {}
    return _vs_cache, stats


def _to_product_card(p: Dict[str, Any], score: Optional[float] = None) -> Dict[str, Any]:
    """Normalize a product dict from the vector store into a frontend-friendly product card.

    The vector store holds dicts that may come from DB serialization or sample data.
    We defensively extract common fields and provide sensible defaults.
    """
    # Prefer canonical image fields but fall back to sample_data naming
    primary_image = p.get("primary_image") or p.get(
        "product_img") or p.get("image_url")
    images = p.get("images")
    if not images:
        images = [primary_image] if primary_image else []

    card = {
        "id": p.get("id"),
        "sku": p.get("sku"),
        "name": p.get("name") or "",
        "description": p.get("description") or "",
        "price": p.get("price", 0.0),
        "rating": p.get("rating", 0.0),
        "tags": p.get("tags") or [],
        "primary_image": primary_image,
        "thumbnail": p.get("image_thumb_url"),
        "images": images,
        "subcategory": p.get("subcategory"),
        "main_category": p.get("main_category"),
        "category_info": p.get("category_info"),
        "times_click_on": p.get("times_click_on", 0),
    }
    if score is not None:
        card["score"] = float(score)
    return card


# Semantic search endpoint


@recom_bp.route('/search', methods=['POST'])
def search_recoms():
    rid = _req_id()
    t0 = _now_ms()
    data = request.get_json() or {}
    query = data.get('query') or data.get('q')
    top_k = int(data.get('top_k', 3))
    if not query:
        return _json_response({'error': 'missing query'}, 400, rid)

    # Simple RAG-style retrieval using the JSON index and in-memory cosine similarity
    vs, stats = _get_vs_cached()
    retrieved = vs.search_similar_products(query, top_k=top_k)
    items = [_to_product_card(prod, score) for prod, score in retrieved]
    elapsed = _now_ms() - t0
    current_app.logger.info(
        f"[recom.search] rid={rid} q='{query}' k={top_k} hits={len(items)} elapsed_ms={elapsed} idx_stats={stats}")
    return _json_response({'results': items, 'count': len(items), 'elapsed_ms': elapsed}, req_id=rid)


# Get similar products for a given product ID
@recom_bp.route('/similar/<int:product_id>', methods=['GET'])
def similar_products(product_id):
    rid = _req_id()
    t0 = _now_ms()
    top_k = request.args.get('top_k', 3, type=int)
    vs, stats = _get_vs_cached()
    sims = vs.find_similar_to_product(product_id, top_k=top_k)
    items = [_to_product_card(prod, score) for prod, score in sims]
    elapsed = _now_ms() - t0
    current_app.logger.info(
        f"[recom.similar] rid={rid} pid={product_id} k={top_k} hits={len(items)} elapsed_ms={elapsed} idx_stats={stats}")
    return _json_response({'results': items, 'count': len(items), 'elapsed_ms': elapsed}, req_id=rid)

# Get products by category


@recom_bp.route('/category/<string:category_name>', methods=['GET'])
def category_products(category_name):
    rid = _req_id()
    t0 = _now_ms()
    top_k = request.args.get('top_k', 3, type=int)
    mode = request.args.get('mode', 'exact')  # exact | semantic | hybrid
    vs, stats = _get_vs_cached()

    results: List[Dict[str, Any]] = []
    lname = category_name.lower()
    if mode in ('exact', 'hybrid'):
        # Prefer explicit field matches when available
        for p in getattr(vs, 'products', []):
            main_cat = (p.get('main_category') or '').lower()
            sub_cat = (p.get('subcategory') or '').lower()
            if lname == main_cat or lname == sub_cat:
                results.append(p)
                if len(results) >= top_k:
                    break
    if mode in ('semantic', 'hybrid') and len(results) < top_k:
        # Fill remaining slots using a semantic query
        needed = top_k - len(results)
        q = f"category: {category_name}"
        sem = vs.search_similar_products(q, top_k=max(needed * 2, needed))
        # Deduplicate by id
        seen = {p.get('id') for p in results}
        for prod, _score in sem:
            pid = prod.get('id')
            if pid not in seen:
                results.append(prod)
                seen.add(pid)
            if len(results) >= top_k:
                break
    # Fallback naive contains if still empty
    if not results:
        for p in getattr(vs, 'products', []):
            text = f"{p.get('name','')} {p.get('description','')} {p.get('main_category','')} {p.get('subcategory','')}".lower()
            if lname in text:
                results.append(p)
                if len(results) >= top_k:
                    break

    items = [_to_product_card(p) for p in results]
    elapsed = _now_ms() - t0
    current_app.logger.info(
        f"[recom.category] rid={rid} name='{category_name}' mode={mode} k={top_k} hits={len(items)} elapsed_ms={elapsed} idx_stats={stats}")
    return _json_response({'results': items, 'count': len(items), 'elapsed_ms': elapsed}, req_id=rid)


@recom_bp.route('/health', methods=['GET'])
def health_check():
    # Check if vector store is initialized
    global _vector_store
    if _vector_store is None:
        with _vector_lock:
            if _vector_store is None:
                try:
                    _vector_store = _init_vector_store()
                except Exception as e:
                    _vector_store = None

    stats = {
        'total_products': 0,
        'embedding_dimension': 0,
        'model_name': None
    }

    # Check if vector store is initialized
    if _vector_store:
        try:
            stats = _vector_store.get_stats()
        except Exception:
            pass

    return jsonify({
        'status': 'ok',
        'vector_store': stats
    })


@recom_bp.route('/answer', methods=['POST'])
def answer():
    rid = _req_id()
    t0 = _now_ms()
    data = request.get_json() or {}
    question = data.get('question') or data.get('query')
    if not question:
        return _json_response({'error': 'missing question'}, 400, rid)
    try:
        res = answer_question(question)
    except Exception as e:
        current_app.logger.exception(f"[recom.answer] rid={rid} failed: {e}")
        return _json_response({'error': str(e)}, 500, rid)
    # Resolve product cards for the retrieved/source ids for direct rendering on the frontend
    vs, _ = _get_vs_cached()
    source_ids = res.get('source_ids') or []
    cards: List[Dict[str, Any]] = []
    for sid in source_ids:
        try:
            prod = vs.get_product_by_id(int(sid))
            if prod:
                # Optionally find similarity score from retrieved metadata
                score_map = {x.get('id'): x.get('score') for x in res.get(
                    '_retrieved', []) if isinstance(x, dict)}
                score = score_map.get(int(sid)) if score_map else None
                cards.append(_to_product_card(prod, score))
        except Exception:
            continue

    elapsed = _now_ms() - t0
    current_app.logger.info(
        f"[recom.answer] rid={rid} hits={len(cards)} elapsed_ms={elapsed}")
    return _json_response({
        'answer': res.get('answer'),
        'source_ids': source_ids,
        'products': cards,
        'raw': res.get('raw'),
        'retrieved': res.get('_retrieved', []),
        'elapsed_ms': elapsed
    }, req_id=rid)


@recom_bp.route('/by_ids', methods=['POST'])
def products_by_ids():
    """Convenience endpoint to resolve a list of product ids into product cards.

    Body: { "ids": [1,2,3] }
    """
    data = request.get_json() or {}
    ids = data.get('ids') or []
    try:
        ids = [int(x) for x in ids]
    except Exception:
        return jsonify({"error": "invalid ids"}), 400

    rid = _req_id()
    vs, _ = _get_vs_cached()
    out = []
    for pid in ids:
        p = vs.get_product_by_id(pid)
        if p:
            out.append(_to_product_card(p))
    return _json_response({"results": out, "count": len(out)}, req_id=rid)


@recom_bp.route('/reindex', methods=['POST'])
def force_reindex():
    """Force reload of the product index file into memory cache."""
    rid = _req_id()
    with _vector_lock:
        global _vs_cache, _vs_cache_mtime
        _vs_cache = load_simple_index()
        try:
            _vs_cache_mtime = os.path.getmtime(INDEX_PATH)
        except Exception:
            _vs_cache_mtime = None
    stats = {}
    try:
        stats = _vs_cache.get_stats() if _vs_cache else {}
    except Exception:
        pass
    current_app.logger.info(f"[recom.reindex] rid={rid} stats={stats}")
    return _json_response({"status": "reloaded", "stats": stats}, req_id=rid)
