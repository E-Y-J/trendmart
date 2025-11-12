from flask import request, jsonify
from schemas.catalog import (
    ProductSchema,
    InventorySchema,
    ReviewSchema,
    CategorySchema,
    SubcategorySchema,
)
from extensions import db
from flask import Blueprint
from models.catalog import Category, Subcategory, Product, Inventory, Review
from werkzeug.security import generate_password_hash
from sqlalchemy import select, delete
from marshmallow import ValidationError

# Define Blueprints
categories_bp = Blueprint('categories', __name__, url_prefix='/categories')
products_bp = Blueprint('products', __name__, url_prefix='/products')
subcategories_bp = Blueprint(
    'subcategories', __name__, url_prefix='/subcategories')

# Product Routes
# Create a new product


@products_bp.route('', methods=['POST'])
def create_product():
    try:
        product_data = request.get_json()
        product_schema = ProductSchema()
        product = product_schema.load(product_data, session=db.session)
        db.session.add(product)
        db.session.commit()
        return jsonify(product_schema.dump(product)), 201
    except ValidationError as err:
        return jsonify(err.messages), 400

# Get all products


@products_bp.route('', methods=['GET'])
def get_products():
    products = Product.query.all()
    product_schema = ProductSchema(many=True)
    return jsonify(product_schema.dump(products)), 200

# Get a single product by id


@products_bp.route('/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"message": "Product not found"}), 404
    product_schema = ProductSchema()
    return jsonify(product_schema.dump(product)), 200

# Update a product


@products_bp.route('/<int:product_id>', methods=['PATCH'])
def update_product(product_id):
    try:
        product = Product.query.get(product_id)
        if not product:
            return jsonify({"message": "Product not found"}), 404

        product_data = request.get_json() or {}
        # Allow partial updates
        product_schema = ProductSchema(partial=True)
        # Load into existing instance to update fields
        updated_product = product_schema.load(
            product_data, instance=product, session=db.session, partial=True)
        db.session.add(updated_product)
        db.session.commit()
        return jsonify(product_schema.dump(updated_product)), 200
    except ValidationError as err:
        return jsonify(err.messages), 400

# Delete a product


@products_bp.route('/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"message": "Product not found"}), 404
    # Remove and commit
    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Product deleted"}), 200


# Category Routes
# List all categories
@categories_bp.route('', methods=['GET'])
def list_categories():
    categories = Category.query.all()
    schema = CategorySchema(many=True)
    return jsonify(schema.dump(categories)), 200

# Get products by category


@categories_bp.route('/<int:category_id>/products', methods=['GET'])
def get_products_by_category(category_id):
    """Return products that belong to the given category via Subcategory relation.

    Note: Product does not have a direct category_id. We must join through
    Subcategory (Product.subcategory_id -> Subcategory.id -> Category.id).
    """
    products = (
        Product.query
        .join(Subcategory, Product.subcategory_id == Subcategory.id)
        .filter(Subcategory.category_id == category_id)
        .all()
    )
    product_schema = ProductSchema(many=True)
    return jsonify(product_schema.dump(products)), 200

# List subcategories for a given category


@categories_bp.route('/<int:category_id>/subcategories', methods=['GET'])
def list_subcategories(category_id):
    subs = Subcategory.query.filter_by(category_id=category_id).all()
    schema = SubcategorySchema(many=True)
    return jsonify(schema.dump(subs)), 200


# Subcategory Routes
@subcategories_bp.route('/<int:subcategory_id>/products', methods=['GET'])
def get_products_by_subcategory(subcategory_id):
    products = Product.query.filter_by(subcategory_id=subcategory_id).all()
    product_schema = ProductSchema(many=True)
    return jsonify(product_schema.dump(products)), 200


# Inventory Routes
# Get current stock of a product
@products_bp.route('/<int:product_id>/inventory', methods=['GET'])
def get_product_inventory(product_id):
    inventory = Inventory.query.filter_by(product_id=product_id).first()
    if not inventory:
        return jsonify({"message": "Inventory not found"}), 404
    inventory_schema = InventorySchema()
    return jsonify(inventory_schema.dump(inventory)), 200


# Review Routes
# Add a review for a product
@products_bp.route('/<int:product_id>/reviews', methods=['POST'])
def add_product_review(product_id):
    try:
        review_data = request.get_json()
        review_data['product_id'] = product_id
        review_schema = ReviewSchema()
        review = review_schema.load(review_data, session=db.session)
        db.session.add(review)
        db.session.commit()
        return jsonify(review_schema.dump(review)), 201
    except ValidationError as err:
        return jsonify(err.messages), 400

# Get all reviews for a product


@products_bp.route('/<int:product_id>/reviews', methods=['GET'])
def get_product_reviews(product_id):
    reviews = Review.query.filter_by(product_id=product_id).all()
    review_schema = ReviewSchema(many=True)
    return jsonify(review_schema.dump(reviews)), 200
