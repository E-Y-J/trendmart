from flask import Blueprint, request, jsonify
from schemas.shopping import (
    CartItemSchema,
    CartItemCreateSchema
)
from extensions import db
from models.shopping import Cart, CartItem
from models.catalog import Product, Inventory
from sqlalchemy import select, delete
from marshmallow import ValidationError

# Define Blueprint
cart_bp = Blueprint('cart', __name__, url_prefix='/cart')

# Cart Routes
# Add item to cart; create cart if one does not exist
@cart_bp.route('/items', methods=['POST'])
def add_item_to_cart():
    try:
        item_data = request.get_json() or {}

        # Determine owning user for the cart. Cart model requires user_id.
        # Accept user_id in the body or as a query parameter.
        user_id = item_data.get('user_id') or request.args.get('user_id')
        if user_id is None:
            return jsonify({"message": "user_id is required to identify the cart owner"}), 400
        try:
            user_id = int(user_id)
        except (TypeError, ValueError):
            return jsonify({"message": "user_id must be an integer"}), 400

        # Load incoming cart item (schema excludes cart_id by design)
        item_schema = CartItemCreateSchema()
        cart_item = item_schema.load(item_data, session=db.session)

        # Ensure product exists
        product = Product.query.get(cart_item.product_id)
        if not product:
            return jsonify({"message": "Product not found"}), 404

        # Find or create the cart for this user
        cart = Cart.query.filter_by(user_id=user_id).first()
        if not cart:
            cart = Cart(user_id=user_id)
            db.session.add(cart)
            db.session.flush()  # assign cart.id so we can reference it

        # Set the cart_id on the item before adding
        cart_item.cart_id = cart.id

        # Merge with existing cart item for same product if present
        existing = CartItem.query.filter_by(
            cart_id=cart.id, product_id=cart_item.product_id
        ).first()
        if existing:
            existing.quantity = (existing.quantity or 0) + (cart_item.quantity or 0)
            db.session.commit()
            result_schema = CartItemSchema()
            return jsonify(result_schema.dump(existing)), 200

        # Otherwise add as new item
        db.session.add(cart_item)
        db.session.commit()
        result_schema = CartItemSchema()
        return jsonify(result_schema.dump(cart_item)), 201
    except ValidationError as err:
        return jsonify(err.messages), 400
    except Exception:
        # Generic catch to avoid leaking internals; log in real app
        return jsonify({"message": "Internal server error"}), 500

# Get all items in a cart
@cart_bp.route('', methods=['GET'])
def get_cart_items():
    # Prefer identifying cart by user_id since Cart is unique per user
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({"message": "user_id query parameter is required"}), 400
    try:
        user_id = int(user_id)
    except (TypeError, ValueError):
        return jsonify({"message": "user_id must be an integer"}), 400

    cart = Cart.query.filter_by(user_id=user_id).first()
    if not cart:
        # return empty list for non-existent cart (idempotent)
        return jsonify([]), 200

    item_schema = CartItemSchema(many=True)
    return jsonify(item_schema.dump(cart.items)), 200

# Remove item from cart
@cart_bp.route('/items/<int:item_id>', methods=['DELETE'])
def remove_item_from_cart(item_id):
    cart_item = CartItem.query.get(item_id)
    if not cart_item:
        return jsonify({"message": "Cart item not found"}), 404

    db.session.delete(cart_item)
    db.session.commit()
    return jsonify({"message": "Item removed from cart"}), 200

# Delete all items in a cart
@cart_bp.route('', methods=['DELETE'])
def clear_cart():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({"message": "user_id query parameter is required"}), 400
    try:
        user_id = int(user_id)
    except (TypeError, ValueError):
        return jsonify({"message": "user_id must be an integer"}), 400

    cart = Cart.query.filter_by(user_id=user_id).first()
    if not cart:
        # Idempotent: nothing to clear
        return jsonify({"message": "Cart cleared"}), 200

    # Bulk delete cart items for this cart
    CartItem.query.filter_by(cart_id=cart.id).delete(synchronize_session=False)
    db.session.commit()
    return jsonify({"message": "Cart cleared"}), 200

# Update item quantity in cart
@cart_bp.route('/items/<int:item_id>', methods=['PATCH'])
def update_cart_item(item_id):
    cart_item = CartItem.query.get(item_id)
    if not cart_item:
        return jsonify({"message": "Cart item not found"}), 404

    item_data = request.get_json() or {}
    if 'quantity' not in item_data:
        return jsonify({"message": "quantity is required"}), 400
    try:
        quantity = int(item_data['quantity'])
    except (TypeError, ValueError):
        return jsonify({"message": "quantity must be an integer"}), 400

    if quantity <= 0:
        # Treat zero or negative as removal
        db.session.delete(cart_item)
        db.session.commit()
        return jsonify({"message": "Item removed from cart"}), 200

    cart_item.quantity = quantity
    db.session.commit()
    item_schema = CartItemSchema()
    return jsonify(item_schema.dump(cart_item)), 200