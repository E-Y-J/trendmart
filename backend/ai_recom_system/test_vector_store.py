from product_vector_store import ProductVectorStore
import sys
import os
import json

# parent directory to backend
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load sample products for testing


def load_sample_products():

    sample_products = [
        {"id": 1, "name": "ZenBook X14", "price": 1299.99,
            "rating": 4.7, "tags": ["ultrabook", "portable", "ssd"]},
        {"id": 2, "name": "MacBook Pro M3", "price": 1899.00,
            "rating": 4.9, "tags": ["apple", "retina", "pro"]},
        {"id": 5, "name": "Acer Predator Helios", "price": 1699.00,
            "rating": 4.6, "tags": ["gaming", "high-performance", "rgb"]},
        {"id": 11, "name": "iPhone 15 Pro", "price": 1199.00,
            "rating": 4.9, "tags": ["apple", "5g", "flagship"]},
        {"id": 21, "name": "PlayStation 5", "price": 499.00,
            "rating": 4.9, "tags": ["sony", "next-gen", "gaming"]},
        {"id": 31, "name": "Optimum Nutrition Whey", "price": 54.99,
            "rating": 4.8, "tags": ["whey", "muscle", "chocolate"]},
        {"id": 71, "name": "Doritos Nacho Cheese", "price": 3.99,
            "rating": 4.5, "tags": ["chips", "snack", "cheese"]},
    ]
    return sample_products


def test_product_vector_store():

    store = ProductVectorStore()

    products = load_sample_products()
    print(f"Adding {len(products)} products to vector store...")
    store.add_products(products)
    print(
        f"Successfully added {len(products)} products. Total products: {len(store.products)}")

    # Show stats
    stats = store.get_stats()
    print(f'Vector_Store_Stats: {stats}')

    # Test semantic searches
    test_queries = [
        "affordable gaming laptop",
        "high-end smartphone with 5G",
        "best protein powder for muscle gain",
        "popular snack food with cheese flavor"
    ]
    print("\nSemantic Search Results:")

    for query in test_queries:
        print(f'\nQuery: "{query}"')
        results = store.search_similar_products(query, top_k=3)

        for i, (product, score) in enumerate(results, 1):
            print(
                f"  {i}. {product['name']} (${product['price']}) - Score: {score:.3f}")

    # Test product-to-product similarity
    print("\nProduct-to-Product Similarity:")

    similar = store.find_similar_to_product(5, top_k=3)
    for i, (product, score) in enumerate(similar, 1):
        print(
            f"  {i}. {product['name']} (${product['price']}) - Score: {score:.3f}")


if __name__ == "__main__":
    test_product_vector_store()
