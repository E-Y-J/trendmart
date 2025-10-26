"""
Product and Category Generator for TrendMart

Generates realistic product catalog data including:
- Categories with SEO-friendly slugs
- Products with proper relationships
- Realistic pricing and descriptions
- Inventory records for each product
"""

from config.sample_data_config import DATA_CONFIG
from models.catalog import Category, Product, Inventory
from extensions import db
import random
from faker import Faker
from typing import List, Dict, Tuple
import sys
import os

# Add parent directory to path to import models
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


fake = Faker()


class ProductGenerator:
    def __init__(self):
        self.categories = []
        self.products = []

    def generate_categories(self) -> List[Category]:
        # Generate product categories from config
        print("🏷️  Generating categories...")

        categories = []
        for cat_data in DATA_CONFIG["categories"]:
            category = Category(
                name=cat_data["name"],
                slug=cat_data["slug"]
            )
            categories.append(category)

        self.categories = categories
        return categories

    def generate_products(self) -> List[Product]:
        # Generate realistic products with proper relationships
        print("📦 Generating products...")

        if not self.categories:
            raise ValueError("Categories must be generated first!")

        products = []
        product_count = DATA_CONFIG["products"]["count"]
        price_ranges = DATA_CONFIG["products"]["price_ranges"]

        # Product name templates for each category
        product_templates = {
            "Electronics": ["Wireless Headphones", "Smart Watch", "Bluetooth Speaker", "Gaming Mouse", "USB-C Cable", "Phone Case", "Tablet Stand", "Wireless Charger"],
            "Fashion & Clothing": ["Cotton T-Shirt", "Denim Jeans", "Running Shoes", "Winter Jacket", "Baseball Cap", "Leather Belt", "Casual Dress", "Sports Bra"],
            "Home & Garden": ["LED Desk Lamp", "Throw Pillow", "Plant Pot", "Wall Clock", "Storage Basket", "Garden Hose", "Outdoor Chair", "Tool Set"],
            "Sports & Outdoors": ["Yoga Mat", "Water Bottle", "Hiking Backpack", "Tennis Racket", "Camping Tent", "Fitness Tracker", "Running Shorts", "Bike Helmet"],
            "Beauty & Health": ["Face Moisturizer", "Vitamin C Serum", "Lip Balm", "Hand Cream", "Shampoo", "Tooth Brush", "Massage Oil", "Hair Mask"],
            "Books & Media": ["Self-Help Book", "Mystery Novel", "Cookbook", "Art Book", "Magazine", "Audio Book", "E-Reader", "Book Light"],
            "Kitchen & Dining": ["Coffee Mug", "Non-Stick Pan", "Cutting Board", "Knife Set", "Blender", "Food Storage", "Wine Glasses", "Dinner Plates"],
            "Toys & Games": ["Board Game", "Puzzle", "Action Figure", "Building Blocks", "Stuffed Animal", "Art Supplies", "Remote Car", "Educational Toy"]
        }

        for i in range(product_count):
            # Pick random category
            category = random.choice(self.categories)
            category_name = category.name

            # Get product name template
            if category_name in product_templates:
                base_name = random.choice(product_templates[category_name])
                # Add variation
                brand = fake.company().split()[0]  # First word of company name
                name = f"{brand} {base_name}"
            else:
                name = fake.catch_phrase()

            # Generate realistic price based on category
            if category_name in price_ranges:
                min_price, max_price = price_ranges[category_name]
                price = round(random.uniform(min_price, max_price), 2)
            else:
                price = round(random.uniform(10, 200), 2)

            # Generate product
            product = Product(
                sku=f"TM-{fake.unique.random_number(digits=6)}",
                name=name,
                description=fake.text(max_nb_chars=300),
                price=price,
                # Placeholder image URL
                product_img=f"https://picsum.photos/400/300?random={i}",
                times_click_on=0,  # Will be updated when we generate behaviors
                tags=self._generate_tags(category_name)
            )

            # Add to category (many-to-many relationship)
            product.categories.append(category)

            products.append(product)

        self.products = products
        return products

    def generate_inventory(self) -> List[Inventory]:
        # Generate inventory records for all products
        print("Generating inventory...")

        if not self.products:
            raise ValueError("Products must be generated first!")

        inventory_records = []
        stock_levels = DATA_CONFIG["inventory"]["stock_levels"]
        restock_prob = DATA_CONFIG["inventory"]["restock_probability"]

        for product in self.products:
            # Determine stock level based on popularity
            stock_type = random.choices(
                ["high", "medium", "low", "out_of_stock"],
                weights=[0.4, 0.4, 0.15, 0.05]  # Most products in stock
            )[0]

            if stock_type == "out_of_stock":
                quantity = 0
                restock = True
            else:
                min_qty, max_qty = stock_levels[stock_type]
                quantity = random.randint(min_qty, max_qty)
                restock = random.random() < restock_prob

            inventory = Inventory(
                product_id=product.id,
                quantity=quantity,
                restock=restock
            )

            inventory_records.append(inventory)

        return inventory_records

    def _generate_tags(self, category_name: str) -> str:
        # Generate relevant tags for products
        base_tags = {
            "Electronics": ["tech", "gadget", "digital", "wireless", "smart"],
            "Fashion & Clothing": ["style", "fashion", "wear", "comfort", "trendy"],
            "Home & Garden": ["home", "decor", "garden", "outdoor", "design"],
            "Sports & Outdoors": ["sport", "fitness", "outdoor", "active", "health"],
            "Beauty & Health": ["beauty", "care", "health", "wellness", "natural"],
            "Books & Media": ["read", "learn", "entertainment", "knowledge", "story"],
            "Kitchen & Dining": ["kitchen", "cook", "dining", "food", "meal"],
            "Toys & Games": ["fun", "play", "game", "kids", "educational"]
        }

        if category_name in base_tags:
            selected_tags = random.sample(
                base_tags[category_name], k=random.randint(2, 4))
        else:
            selected_tags = ["popular", "quality"]

        return ", ".join(selected_tags)


def generate_catalog_data():
    # Main function to generate all catalog data
    generator = ProductGenerator()

    # Generate in correct order (categories first, then products)
    categories = generator.generate_categories()
    products = generator.generate_products()
    inventory = generator.generate_inventory()

    return {
        "categories": categories,
        "products": products,
        "inventory": inventory
    }


if __name__ == "__main__":
    # Test the generator
    data = generate_catalog_data()
    print(f"Generated {len(data['categories'])} categories")
    print(f"Generated {len(data['products'])} products")
    print(f"Generated {len(data['inventory'])} inventory records")
