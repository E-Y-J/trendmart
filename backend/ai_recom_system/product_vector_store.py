import numpy as np
import json
from typing import List, Dict, Any, Tuple, Optional
from sentence_transformers import SentenceTransformer


class ProductVectorStore:
    '''A simple in-memory vector store for product embeddings.'''

    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        '''Initialize the vector store with a specified sentence transformer model.

        Args:
            model_name: Name of the sentence transformer model to use.
        '''
        self.model_name = model_name
        # Initialize the sentence transformer model
        self.sentence_model = SentenceTransformer(model_name)
        self.products = []
        self.product_embeddings = []

        # Mapping from product ID to index in embeddings list
        self.id_to_index = {}

    def create_product_text(self, product: Dict[str, Any]) -> str:
        """
        Create a comprehensive text representation of a product for embedding.
        Enhanced with category context and product type identification.
        """
        # Extract product information
        name = product.get('name', '')
        tags = product.get('tags', [])
        price = product.get('price', 0)
        rating = product.get('rating', 0)

        # Infer product category from name and tags
        category_context = self._get_category_context(name, tags)

        # Create rich text representation
        tag_text = ' '.join(tags) if tags else ''
        price_range = self._get_price_range(price)
        rating_text = self._get_rating_text(rating)

        # Enhanced text with category context
        product_text = f"{name} {category_context} {tag_text} {price_range} {rating_text} product"

        return product_text.lower().strip()

    def _get_category_context(self, name: str, tags: List[str]) -> str:
        """Add explicit category context to distinguish product types."""
        name_lower = name.lower()
        tag_text = ' '.join(tags).lower()

        # Text enrichment based on keywords
        # Electronics categories
        if any(word in name_lower for word in ['iphone', 'samsung', 'pixel', 'oneplus']):
            return "smartphone mobile phone cellular device communication"
        elif any(word in name_lower for word in ['macbook', 'laptop', 'notebook', 'zenbook']):
            return "laptop computer notebook portable computing"
        elif any(word in name_lower for word in ['playstation', 'xbox', 'nintendo', 'console']):
            return "gaming console video game entertainment system"

        # Health & Nutrition
        elif any(word in tag_text for word in ['whey', 'protein', 'muscle']):
            return "protein supplement nutrition fitness health powder"
        elif any(word in tag_text for word in ['probiotic', 'digestive', 'gut']):
            return "digestive supplement health wellness probiotic capsule"
        elif any(word in tag_text for word in ['vitamin', 'multivitamin', 'supplement']):
            return "vitamin supplement nutrition health daily wellness"

        # Food & Snacks
        elif any(word in tag_text for word in ['chips', 'snack', 'cheese']):
            return "snack food chips crispy salty taste treat"
        elif any(word in tag_text for word in ['protein-bar', 'bar', 'ready-to-drink']):
            return "protein snack nutrition bar convenient food"

        return "general merchandise product item"

    def _get_price_range(self, price: float) -> str:
        """Categorize price into range for better semantic understanding.

        Args:
            price: Product price
            Returns:
                Descriptive price range text
    """
        if price < 100:
            return "budget affordable cheap"
        elif price < 500:
            return "mid-range moderate"
        elif price < 1000:
            return "premium quality"
        else:
            return "luxury high-end expensive"

    def _get_rating_text(self, rating: float) -> str:
        """Convert rating to descriptive text.

        Args:
            rating: Product rating (0-5 scale)
            Returns:
                Descriptive rating text"""
        if rating >= 4.5:
            return "highly rated excellent"
        elif rating >= 4.0:
            return "good quality rated"
        elif rating >= 3.5:
            return "decent quality"
        else:
            return "affordable"

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
            embedding = self.sentence_model.encode(
                product_text, convert_to_tensor=False)

            self.products.append(product)
            self.product_embeddings.append(embedding)
            self.id_to_index[product['id']] = len(self.products) - 1

        # Print confirmation message for testing purposes
        print(
            f"Successfully added {len(products)} products. Total products: {len(self.products)}")

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
        query_embedding = self.sentence_model.encode(
            query, convert_to_tensor=False)

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
