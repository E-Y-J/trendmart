"""
Catalog Models

This module contains all database models related to the product catalog system.
Includes categories, products, inventory, and reviews functionality.

Models:
    - Category: Product categorization
    - Product: Core product information
    - Inventory: Stock management per product
    - Review: Customer product reviews and ratings
"""

from extensions import db
from sqlalchemy import CheckConstraint, UniqueConstraint

# Association table for many-to-many relationship between Product and Category
# This enables products to belong to multiple categories and vice versa
product_categories = db.Table('product_categories',
                              db.Column('product_id', db.Integer, db.ForeignKey(
                                  'products.id'), primary_key=True),
                              db.Column('category_id', db.Integer, db.ForeignKey(
                                  'categories.id'), primary_key=True)
                              )


class Category(db.Model):
    """
    Product Category Model

    Represents product categories for organizing products in the catalog.
    Categories can have multiple products and products can belong to multiple categories.

    Attributes:
        id (int): Primary key, auto-incrementing category identifier
        name (str): Unique category name for display (max 100 chars)
        slug (str): URL-friendly version of name, unique and indexed for SEO
    """
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False, index=True)

    # Relationships
    products = db.relationship(
        'Product', secondary=product_categories, back_populates='categories')


class Product(db.Model):
    """
    Product Model

    Core model representing products in the e-commerce catalog.
    Contains all essential product information and relationships.

    Attributes:
        id (int): Primary key, unique product identifier
        sku (str): Stock Keeping Unit, unique product code for inventory
        name (str): Product display name, indexed for search performance
        description (str): Detailed product description, unlimited text
        price (float): Product price in default currency, required field
        product_img (str): URL/path to main product image
        times_click_on (int): Analytics counter for product page views
        tags (str): Comma-separated tags for search and filtering
    """
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    sku = db.Column(db.String(50), unique=True, nullable=False, index=True)
    name = db.Column(db.String(255), nullable=True, index=True)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    product_img = db.Column(db.String(500))
    times_click_on = db.Column(db.Integer, default=0, nullable=False)
    tags = db.Column(db.String(255))

    # Relationships
    # Many-to-many: Products can belong to multiple categories
    categories = db.relationship(
        'Category', secondary=product_categories, back_populates='products')

    # One-to-many: Product can have multiple reviews, delete reviews if product deleted
    reviews = db.relationship(
        'Review', back_populates='product', cascade='all, delete-orphan')

    # One-to-one: Each product has one inventory record, delete inventory if product deleted
    inventory = db.relationship(
        'Inventory', back_populates='product', uselist=False, cascade='all, delete-orphan')

    # One-to-many: Product can be in multiple carts (no cascade - preserve cart history)
    cart_items = db.relationship('CartItem', back_populates='product')

    # One-to-many: Product can be in multiple orders (no cascade - preserve order history)
    order_items = db.relationship('OrderItem', back_populates='product')

    # One-to-many: Product can have multiple recommendation scores
    recommendations = db.relationship(
        'Recommendation', back_populates='product')


class Inventory(db.Model):
    """
    Inventory Management Model

    Tracks stock levels and restock status for products.
    One-to-one relationship with Product (each product has one inventory record).

    Attributes:
        product_id (int): Primary key and foreign key to Product
        quantity (int): Current stock level, defaults to 0
        restock (bool): Flag indicating if product needs restocking
    """
    __tablename__ = 'inventory'

    product_id = db.Column(
        db.Integer, db.ForeignKey('products.id', ondelete='CASCADE'), primary_key=True)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    restock = db.Column(db.Boolean, default=False, nullable=False)

    # Relationships
    product = db.relationship('Product', back_populates='inventory')


class Review(db.Model):
    """
    Product Review Model

    Stores customer reviews and ratings for products.
    Enforces business rules: one review per user per product, rating 0-5 scale.

    Attributes:
        id (int): Primary key, unique review identifier
        product_id (int): Foreign key to Product, indexed for performance
        user_id (int): Foreign key to User, indexed for performance  
        rating (float): Numerical rating between 0-5 (enforced by constraint)
        title (str): Review headline/summary (max 500 chars)
        comment (str): Detailed review text, unlimited length
        created_on (datetime): Timestamp when review was created

    Constraints:
        - Rating must be between 0 and 5 (database constraint)
        - One review per user per product (unique constraint)
    """
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey(
        "products.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False, index=True)
    rating = db.Column(db.Float, nullable=False)
    title = db.Column(db.String(500), nullable=False)
    comment = db.Column(db.Text)
    created_on = db.Column(db.DateTime, default=db.func.now(), nullable=False)

    __table_args__ = (
        CheckConstraint('rating >= 0 AND rating <= 5',
                        name='ck_review_rating_0_5'),
        UniqueConstraint('product_id', 'user_id',
                         name='uq_review_product_user')
    )

    # Relationships
    product = db.relationship('Product', back_populates='reviews')
    user = db.relationship('User', back_populates='reviews')
