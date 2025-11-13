export const userData = {
    "schema_version": "1.1",
    "generated_at": "2025-10-31T23:59:00Z",
    "products": [
        {
            "id": 61,
            "name": "Optimum Nutrition Gold Standard Whey",
            "description": "Whey protein powder for muscle support.",
            "price": 54.99,
            "rating": 4.8,
            "tags": ["form-powder", "protein-whey", "macro-high-protein"],
            "category_info": { "main_category": "Supplements", "subcategory": "Protein Powder" }
        },
        {
            "id": 13,
            "name": "ASUS ROG Zephyrus G14",
            "description": "Compact 14-inch gaming laptop with powerful performance.",
            "price": 1899.0,
            "rating": 4.6,
            "tags": ["brand-asus", "os-windows", "gpu-rtx-4070"],
            "category_info": { "main_category": "Electronics", "subcategory": "Laptops" }
        },
        {
            "id": 37,
            "name": "OnePlus Nord N30",
            "description": "Affordable Android phone with 120Hz display.",
            "price": 299.0,
            "rating": 4.6,
            "tags": ["platform-android", "display-120hz"],
            "category_info": { "main_category": "Electronics", "subcategory": "Phones" }
        },
        {
            "id": 38,
            "name": "Apple iPhone 15 Pro",
            "description": "Flagship iPhone with titanium design.",
            "price": 1199.0,
            "rating": 4.3,
            "tags": ["platform-ios", "titanium", "usb-c"],
            "category_info": { "main_category": "Electronics", "subcategory": "Phones" }
        },
        {
            "id": 41,
            "name": "Sony PlayStation 5",
            "description": "Next-gen gaming console with 4K gaming.",
            "price": 499.0,
            "rating": 4.5,
            "tags": ["ecosystem-sony", "gen-current"],
            "category_info": { "main_category": "Electronics", "subcategory": "Gaming Consoles" }
        },
        {
            "id": 12,
            "name": "HP Victus 16",
            "description": "Value gaming laptop with RTX 4050.",
            "price": 1049.0,
            "rating": 4.7,
            "tags": ["brand-hp", "gpu-rtx-4050"],
            "category_info": { "main_category": "Electronics", "subcategory": "Laptops" }
        },
        {
            "id": 60,
            "name": "Panic Playdate Season 1 Bundle",
            "description": "Handheld console bundle with indie games.",
            "price": 199.0,
            "rating": 4.7,
            "tags": ["portable", "bundle"],
            "category_info": { "main_category": "Electronics", "subcategory": "Gaming Consoles" }
        },
        {
            "id": 43,
            "name": "Sony PlayStation 5 Pro",
            "description": "Enhanced console targeting 4K120.",
            "price": 699.0,
            "rating": 4.5,
            "tags": ["ecosystem-sony", "target-4k120"],
            "category_info": { "main_category": "Electronics", "subcategory": "Gaming Consoles" }
        }
    ],
    "users": [
        {
            "user_id": 1,
            "age": 28,
            "gender": "female",
            "location": "New York",
            "income_range": "50k-75k",
            "preferences": ["electronics", "fashion"],
            "created_at": "2024-01-15"
        },
        {
            "user_id": 2,
            "age": 35,
            "gender": "male",
            "location": "Chicago",
            "income_range": "75k-100k",
            "preferences": ["gaming", "computers"],
            "created_at": "2024-02-20"
        },
        {
            "user_id": 3,
            "age": 22,
            "gender": "female",
            "location": "Los Angeles",
            "income_range": "25k-50k",
            "preferences": ["beauty", "fashion"],
            "created_at": "2024-03-10"
        },
        {
            "user_id": 4,
            "age": 41,
            "gender": "male",
            "location": "Austin",
            "income_range": "100k-150k",
            "preferences": ["electronics", "home appliances"],
            "created_at": "2024-04-05"
        },
        {
            "user_id": 5,
            "age": 30,
            "gender": "female",
            "location": "Seattle",
            "income_range": "50k-75k",
            "preferences": ["fitness", "wearables"],
            "created_at": "2024-05-12"
        }
    ],
    "interactions": [
        { "user_id": 1, "product_id": 38, "interaction_type": "view", "timestamp": "2024-10-01T14:30:00Z", "duration_seconds": 45 },
        { "user_id": 1, "product_id": 38, "interaction_type": "purchase", "timestamp": "2024-10-01T15:00:00Z", "quantity": 1, "rating_given": 5 },
        { "user_id": 2, "product_id": 13, "interaction_type": "add_to_cart", "timestamp": "2024-10-03T16:15:00Z" },
        { "user_id": 2, "product_id": 13, "interaction_type": "rating", "timestamp": "2024-10-03T18:00:00Z", "rating_given": 4 },
        { "user_id": 3, "product_id": 61, "interaction_type": "view", "timestamp": "2024-10-05T09:56:00Z", "duration_seconds": 60 },
        { "user_id": 3, "product_id": 61, "interaction_type": "rating", "timestamp": "2024-10-05T10:00:00Z", "rating_given": 4 },
        { "user_id": 4, "product_id": 41, "interaction_type": "view", "timestamp": "2024-10-06T11:10:00Z", "duration_seconds": 90 },
        { "user_id": 4, "product_id": 12, "interaction_type": "view", "timestamp": "2024-10-06T11:45:00Z", "duration_seconds": 75 },
        { "user_id": 5, "product_id": 37, "interaction_type": "view", "timestamp": "2024-10-07T09:20:00Z", "duration_seconds": 120 },
        { "user_id": 5, "product_id": 37, "interaction_type": "add_to_cart", "timestamp": "2024-10-07T09:25:00Z" },
        { "user_id": 1, "product_id": 60, "interaction_type": "view", "timestamp": "2024-10-08T10:30:00Z", "duration_seconds": 35 },
        { "user_id": 2, "product_id": 43, "interaction_type": "view", "timestamp": "2024-10-08T12:05:00Z", "duration_seconds": 60 }
    ],
    "purchases": [
        { "user_id": 1, "product_id": 38, "purchase_date": "2024-10-01", "quantity": 1, "price_paid": 1199.0, "rating_given": 5, "review_text": "Amazing camera quality." },
        { "user_id": 2, "product_id": 13, "purchase_date": "2024-10-03", "quantity": 1, "price_paid": 1799.99, "rating_given": 4, "review_text": "Excellent gaming laptop for the price." },
        { "user_id": 3, "product_id": 61, "purchase_date": "2024-10-05", "quantity": 2, "price_paid": 79.98, "rating_given": 4, "review_text": "Nice protein powder, mixes well." },
        { "user_id": 5, "product_id": 37, "purchase_date": "2024-10-07", "quantity": 1, "price_paid": 299.0, "rating_given": 5, "review_text": "Great value for features." },
        { "user_id": 1, "product_id": 60, "purchase_date": "2024-10-09", "quantity": 1, "price_paid": 279.99, "rating_given": 5, "review_text": "Fun handheld bundle." },
        { "user_id": 2, "product_id": 43, "purchase_date": "2024-10-10", "quantity": 1, "price_paid": 499.0, "rating_given": 5, "review_text": "Load times are insane." }
    ],
    "search_queries": [
        { "user_id": 1, "query": "best gaming laptop under 2000", "timestamp": "2024-10-01T10:00:00Z", "results_clicked": [13], "products_purchased": [] },
        { "user_id": 2, "query": "flagship smartphone 256gb", "timestamp": "2024-10-02T12:20:00Z", "results_clicked": [38], "products_purchased": [38] },
        { "user_id": 4, "query": "best next-gen console", "timestamp": "2024-10-06T09:30:00Z", "results_clicked": [41], "products_purchased": [] },
        { "user_id": 5, "query": "best budget android phone", "timestamp": "2024-10-07T08:55:00Z", "results_clicked": [37], "products_purchased": [37] },
        { "user_id": 1, "query": "handheld console bundle", "timestamp": "2024-10-09T09:40:00Z", "results_clicked": [60], "products_purchased": [60] }
    ],
    "sessions": [
        {
            "session_id": 10001,
            "user_id": 1,
            "products_viewed": [38, 60],
            "view_durations": [30, 120],
            "session_start": "2024-10-01T14:00:00Z",
            "session_end": "2024-10-01T14:30:00Z"
        },
        {
            "session_id": 10002,
            "user_id": 3,
            "products_viewed": [61],
            "view_durations": [75],
            "session_start": "2024-10-05T09:00:00Z",
            "session_end": "2024-10-05T09:20:00Z"
        },
        {
            "session_id": 10003,
            "user_id": 4,
            "products_viewed": [41, 12],
            "view_durations": [90, 75],
            "session_start": "2024-10-06T11:00:00Z",
            "session_end": "2024-10-06T12:00:00Z"
        },
        {
            "session_id": 10004,
            "user_id": 2,
            "products_viewed": [13, 43],
            "view_durations": [60, 90],
            "session_start": "2024-10-08T12:00:00Z",
            "session_end": "2024-10-08T13:00:00Z"
        },
        {
            "session_id": 10005,
            "user_id": 5,
            "products_viewed": [37],
            "view_durations": [120],
            "session_start": "2024-10-07T09:00:00Z",
            "session_end": "2024-10-07T09:45:00Z"
        }
    ]
};
