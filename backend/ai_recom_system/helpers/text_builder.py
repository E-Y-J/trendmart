from typing import Dict, Any

from .category_context import get_category_context
from .price import get_price_range
from .rating import get_rating_text


def create_product_text(product: Dict[str, Any]) -> str:
    '''Compose the text used for embedding a product.
    Expects a product dict with keys like 'name', 'tags', 'price', 'rating'.
    '''
    # Extract product information
    name = product.get('name', '') or ''
    tags = product.get('tags', []) or []
    price = product.get('price', 0)
    rating = product.get('rating', 0)

    # Get enriched context
    category_context = get_category_context(name, tags)
    tag_text = ' '.join(tags) if tags else ''
    # Pass numeric values to the price/rating helpers
    price_range = get_price_range(price)
    rating_text = get_rating_text(rating)

    product_text = f'{name}, {category_context}, {tag_text}, {price_range}, {rating_text} product'
    return product_text.lower().strip()
