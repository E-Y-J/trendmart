import numpy as np
import json
from typing import List, Dict, Any, Tuple, Optional
from .helpers.text_builder import create_product_text
from .embeddings_backend import make_backend, BaseEmbeddingBackend


class ProductVectorStore:
    '''A simple in-memory vector store for product embeddings.'''

    def __init__(self, model_name: str = 'all-MiniLM-L6-v2', backend: BaseEmbeddingBackend | None = None):
        '''Initialize the vector store with a specified embedding backend.

        Args:
            model_name: Name of the sentence transformer model to use (when using HF backend).
            backend: Optional embedding backend; if None, chosen via env (HF vs Ollama).
        '''
        self.model_name = model_name
        self.backend = backend or make_backend()
        self.products: List[Dict[str, Any]] = []
        self.product_embeddings: List[List[float]] = []

        # Mapping from product ID to index in embeddings list
        self.id_to_index: Dict[int, int] = {}

    def add_products(self, products: List[Dict[str, Any]], category_info: Dict[str, Any] = None):
        '''Add products to the vector store and compute their embeddings.

        Args:
            products: List of product dictionaries to add.
            category_info: Optional dictionary mapping product IDs to category details.
        '''
        for product in products:
            if category_info:
                product['category_info'] = category_info.get(product['id'], '')
                product['main_category'] = category_info.get(
                    product['id'], '').get('main_category', '')

            # Create text representation and compute embedding
            product_text = self.create_product_text(product)
            embedding = self.backend.embed(product_text)

            self.products.append(product)
            self.product_embeddings.append(embedding)
            self.id_to_index[product['id']] = len(self.products) - 1

        # Print confirmation message for testing purposes
        print(
            f"Successfully added {len(products)} products. Total products: {len(self.products)}")

    def set_products_and_embeddings(self, products: List[Dict[str, Any]], embeddings: List[List[float]]):
        """Directly set products and their precomputed embeddings.

        Args:
            products: List of product dicts.
            embeddings: List of embedding vectors aligned by index with products.

        Raises:
            ValueError: if lengths don't match or embeddings are malformed.
        """
        if len(products) != len(embeddings):
            raise ValueError(
                "products and embeddings must have the same length")
        # Basic validation that each embedding is a list/sequence of numbers
        for i, emb in enumerate(embeddings):
            if not isinstance(emb, (list, tuple)) or (emb and not isinstance(emb[0], (int, float))):
                raise ValueError(
                    f"embedding at index {i} is not a numeric vector")

        self.products = list(products)
        self.product_embeddings = [list(vec) for vec in embeddings]
        self.id_to_index = {}
        for idx, p in enumerate(self.products):
            if 'id' in p:
                self.id_to_index[p['id']] = idx

    def create_product_text(self, product: Dict[str, Any]) -> str:
        """Delegate to the helper text builder to compose embedding text."""
        return create_product_text(product)

    def search_similar_products(self, query: str, top_k: int = 10,
                                exclude_ids: List[int] = None) -> List[Tuple[Dict[str, Any], float]]:
        """
        Search for products similar to the query using semantic similarity.

        Args:
            query: Search query (can be natural language)
            top_k: Number of results to return
            exclude_ids: Product IDs to exclude from results

        Returns:
            List of tuples (product, similarity_score)
        """
        if not self.products:
            return []

        # Generate query embedding
        query_embedding = self.backend.embed(query)

        # Calculate similarities with all products
        similarities = []
        for i, product_embedding in enumerate(self.product_embeddings):
            # Calculate cosine similarity
            similarity = self._cosine_similarity(
                query_embedding, product_embedding)
            similarities.append((i, similarity))

        # Sort by similarity (highest first)
        similarities.sort(key=lambda x: x[1], reverse=True)

        # Filter results and build response
        results = []
        exclude_indices = set()

        # Convert exclude_ids to indices
        if exclude_ids:
            exclude_indices = {
                self.id_to_index[pid] for pid in exclude_ids if pid in self.id_to_index}

        for i, similarity in similarities:
            if len(results) >= top_k:
                break

            if i not in exclude_indices:
                product = self.products[i]
                results.append((product, similarity))

        return results

    def _cosine_similarity(self, vec1, vec2):
        """Calculate cosine similarity between two vectors."""
        # Convert to numpy arrays
        vec1 = np.array(vec1)
        vec2 = np.array(vec2)

        # Calculate cosine similarity
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)

        if norm1 == 0 or norm2 == 0:
            return 0

        return dot_product / (norm1 * norm2)

    def get_product_by_id(self, product_id: int) -> Optional[Dict[str, Any]]:
        # Get product by ID.
        if product_id in self.id_to_index:
            index = self.id_to_index[product_id]
            return self.products[index]
        return None

    def find_similar_to_product(self, product_id: int, top_k: int = 10) -> List[Tuple[Dict[str, Any], float]]:
        """
        Find products similar to a given product.

        Args:
            product_id: ID of the reference product
            top_k: Number of similar products to return

        Returns:
            List of tuples (product, similarity_score)
        """
        product = self.get_product_by_id(product_id)
        if not product:
            return []

        # Create text from the product and search for similar ones
        product_text = self.create_product_text(product)
        return self.search_similar_products(product_text, top_k + 1, exclude_ids=[product_id])

    def get_stats(self) -> Dict[str, Any]:
        # Get statistics about the vector store.
        return {
            'total_products': len(self.products),
            'embedding_dimension': len(self.product_embeddings[0]) if self.product_embeddings else 0,
            'model_name': self.model_name
        }
