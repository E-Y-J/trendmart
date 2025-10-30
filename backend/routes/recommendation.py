from flask import Blueprint, request, jsonify, current_app
import threading
from typing import List, Dict, Any

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
    data = request.get_json()
    query = data.get('query')
    top_k = data.get('top_k', 3)

    return jsonify({'message': f'Semantic search for query: {query} with top_k={top_k} not yet implemented.'})


# Get similar products for a given product ID
@recom_bp.route('/similar/<int:product_id>', methods=['GET'])
def similar_products(product_id):
    top_k = request.args.get('top_k', 3, type=int)

    return jsonify({'message': f'Get {top_k} similar products for product_id: {product_id} not yet implemented.'})

# Get products by category


@recom_bp.route('/category/<string:category_name>', methods=['GET'])
def category_products(category_name):
    top_k = request.args.get('top_k', 3, type=int)

    return jsonify({'message': f'Get {top_k} products for category: {category_name} not yet implemented.'})


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
