"""
TrendMart Sample Data Generation Configuration

This file defines all parameters for generating realistic e-commerce data
optimized for building recommendation systems.
"""

DATA_CONFIG = {
    # User generation settings
    "users": {
        "count": 200,  # Good balance for recommendation patterns
        "roles": {
            "customer": 0.95,
            "admin": 0.05
        },
        "activity_levels": {
            "high": 0.2,    # 20% very active users
            "medium": 0.5,  # 50% moderately active
            "low": 0.3      # 30% occasional browsers
        }
    },

    # Product catalog subject to change on team review
    "categories": [
        {"name": "Electronics", "slug": "electronics"},
        {"name": "Fashion & Clothing", "slug": "fashion"},
        {"name": "Home & Garden", "slug": "home-garden"},
        {"name": "Sports & Outdoors", "slug": "sports"},
        {"name": "Beauty & Health", "slug": "beauty"},
        {"name": "Books & Media", "slug": "books"},
        {"name": "Kitchen & Dining", "slug": "kitchen"},
        {"name": "Toys & Games", "slug": "toys"}
    ],

    "products": {
        "count": 100,  # Sweet spot for variety without overwhelming
        "price_ranges": {
            "Electronics": (25, 1200),
            "Fashion & Clothing": (10, 200),
            "Home & Garden": (15, 500),
            "Sports & Outdoors": (20, 800),
            "Beauty & Health": (8, 150),
            "Books & Media": (5, 60),
            "Kitchen & Dining": (12, 300),
            "Toys & Games": (10, 150)
        },
        "popularity_distribution": {
            "bestseller": 0.15,  # 15% popular products
            "regular": 0.70,     # 70% normal products
            "niche": 0.15        # 15% rarely viewed
        }
    },

    # User behavior patterns (critical for recommendations)
    "behaviors": {
        "sessions_per_user": {
            "high": (8, 20),    # Active users
            "medium": (3, 8),   # Regular users
            "low": (1, 3)       # Occasional users
        },
        "views_per_session": (2, 15),
        "purchase_probability": 0.12,  # 12% of views lead to reviews
        "review_probability": 0.65,    # 65% of purchases get reviewed
        "return_customer_rate": 0.35   # 35% become repeat customers
    },

    # Inventory settings
    "inventory": {
        "stock_levels": {
            "high": (50, 200),
            "medium": (10, 50),
            "low": (1, 10),
            "out_of_stock": 0
        },
        "restock_probability": 0.15
    }
}

# Recommendation system specific settings
RECOMMENDATION_CONFIG = {
    "similarity_factors": [
        "category_overlap",
        "price_similarity",
        "rating_correlation",
        "user_behavior_patterns"
    ],
    "min_interactions_for_recommendations": 5,
    "target_recommendations_per_user": 10
}
