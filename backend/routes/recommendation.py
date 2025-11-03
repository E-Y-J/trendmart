from flask import Blueprint, request, jsonify, current_app
import threading
from typing import List, Dict, Any
from ai_recom_system.rag_service import answer_question, load_simple_index

# Blueprint placed here to prevent circular imports
recom_bp = Blueprint('recommendation', __name__, url_prefix='/recommendations')

_vector_store = None  # Placeholder for vector store initialization
_vector_lock = threading.Lock()


def _init_vector_store():
    from ai_recom_system.product_vector_store import ProductVectorStore

    model_name = current_app.config.get('EMBED_MODEL', 'all-MiniLM-L6-v2')
    vs = ProductVectorStore(model_name=model_name)
    return vs
# Semantic search endpoint


@recom_bp.route('/search', methods=['POST'])
def search_recoms():
    data = request.get_json() or {}
    query = data.get('query') or data.get('q')
    top_k = int(data.get('top_k', 3))
    if not query:
        return jsonify({'error': 'missing query'}), 400

    # Simple RAG-style retrieval using the JSON index and in-memory cosine similarity
    vs = load_simple_index()
    retrieved = vs.search_similar_products(query, top_k=top_k)
    items = []
    for prod, score in retrieved:
        items.append({
            'id': prod.get('id'),
            'name': prod.get('name'),
            'description': prod.get('description'),
            'score': float(score)
        })
    return jsonify({'results': items, 'count': len(items)})


# Get similar products for a given product ID
@recom_bp.route('/similar/<int:product_id>', methods=['GET'])
def similar_products(product_id):
    top_k = request.args.get('top_k', 3, type=int)
    vs = load_simple_index()
    sims = vs.find_similar_to_product(product_id, top_k=top_k)
    items = []
    for prod, score in sims:
        items.append({
            'id': prod.get('id'),
            'name': prod.get('name'),
            'description': prod.get('description'),
            'score': float(score)
        })
    return jsonify({'results': items, 'count': len(items)})

# Get products by category


@recom_bp.route('/category/<string:category_name>', methods=['GET'])
def category_products(category_name):
    top_k = request.args.get('top_k', 3, type=int)
    # For now, filter loaded products by simple string contains on category fields if present.
    vs = load_simple_index()
    # naive filtering: find products that contain category_name in name/description
    results = []
    for p in getattr(vs, 'products', []):
        text = f"{p.get('name','')} {p.get('description','')} {p.get('main_category','')} {p.get('category_info','')}".lower()
        if category_name.lower() in text:
            results.append(p)
        if len(results) >= top_k:
            break
    items = [{'id': p.get('id'), 'name': p.get(
        'name'), 'description': p.get('description')} for p in results]
    return jsonify({'results': items, 'count': len(items)})


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
    data = request.get_json() or {}
    question = data.get('question') or data.get('query')
    if not question:
        return jsonify({'error': 'missing question'}), 400
    try:
        res = answer_question(question)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify({'answer': res.get('answer'), 'source_ids': res.get('source_ids', []), 'raw': res.get('raw'), 'retrieved': res.get('_retrieved', [])})
