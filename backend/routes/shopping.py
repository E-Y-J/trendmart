from flask import request, jsonify, Blueprint
from schemas.shopping import CartSchema, CartItemSchema, OrderCreateSchema, OrderSchema, OrderItemCreateSchema, OrderItemSchema
from models.registration import User
from models.catalog import Product
from models.shopping import Cart, CartItem, Order, OrderItem
from marshmallow import ValidationError
from sqlalchemy import select, delete
from extensions import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Blueprint, request, jsonify
from werkzeug.exceptions import BadRequest
from models.shopping import Order
from utils.payment_service import PaymentService

order_bp = Blueprint("order", __name__, url_prefix="/orders")


def _error(code: str, message: str, status: int):
    return jsonify({"error": code, "message": message}), status


@order_bp.route('/<int:order_id>/payments/intents', methods=['POST'])
def order_payment_intent(order_id):
    currency = (request.get_json(silent=True) or {}
                ).get('currency', 'usd').lower()
    order = Order.query.get(order_id)

    if not order:
        return _error('order_not_found', f'Order {order_id} not found', 404)

    amount_cents = int(round((order.total or 0.0) * 100))
    if amount_cents <= 0:
        return _error('bad_request', 'Order total must be greater than zero', 400)

    result = PaymentService.create_payment_intent(
        order_id=order_id,
        amount=amount_cents,
        currency=currency,
        metadata={'source': f'order:{order_id}'}
    )

    return jsonify(result), 200


cart_bp = Blueprint('cart', __name__, url_prefix='/cart')

# Add item to cart


@cart_bp.route('/items', methods=['POST'])
@jwt_required()
def add_to_cart():
    """
    Add a product to the user's cart.
    Creates cart automatically if it doesn't exist.
    Updates quantity if product already in cart.
    """
    try:
        current_user_id = int(get_jwt_identity())
        request_data = request.get_json()

        # Validate required fields
        if not request_data or 'product_id' not in request_data:
            return jsonify({"error": "product_id is required"}), 400

        product_id = request_data['product_id']
        quantity = request_data.get('quantity', 1)

        # Validate quantity
        if quantity <= 0:
            return jsonify({"error": "Quantity must be positive"}), 400

        # Check if product exists
        product = Product.query.get(product_id)
        if not product:
            return jsonify({"error": "Product not found"}), 404

        # Get or create user's cart
        cart = Cart.query.filter_by(user_id=current_user_id).first()
        if not cart:
            cart = Cart(user_id=current_user_id)
            db.session.add(cart)
            db.session.flush()  # Get cart ID

        # Check if item already exists in cart
        existing_item = CartItem.query.filter_by(
            cart_id=cart.id,
            product_id=product_id
        ).first()

        if existing_item:
            # Update quantity of existing item
            existing_item.quantity += quantity
            existing_item.price_per_unit = product.price  # Update price
            cart.last_updated_at = db.func.now()
            item_to_return = existing_item
        else:
            # Add new item to cart
            new_item = CartItem(
                cart_id=cart.id,
                product_id=product_id,
                quantity=quantity,
                price_per_unit=product.price
            )
            db.session.add(new_item)
            cart.last_updated_at = db.func.now()
            item_to_return = new_item

        db.session.commit()

        return jsonify({
            "message": "Item added to cart successfully",
            "cart_item": CartItemSchema().dump(item_to_return),
            "cart_total": cart.cart_total_value
        }), 201

    except ValidationError as err:
        return jsonify(err.messages), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to add item to cart: {str(e)}"}), 500


# Update cart item quantity
@cart_bp.route('/items/<int:item_id>', methods=['PATCH'])
@jwt_required()
def update_cart_item(item_id):
    """
    Update quantity of a specific cart item.
    """
    try:
        current_user_id = int(get_jwt_identity())
        request_data = request.get_json()

        if not request_data or 'quantity' not in request_data:
            return jsonify({"error": "quantity is required"}), 400

        quantity = request_data['quantity']

        if quantity <= 0:
            return jsonify({"error": "Quantity must be positive"}), 400

        # Find cart item belonging to current user
        cart_item = (db.session.query(CartItem)
                     .join(Cart, CartItem.cart_id == Cart.id)
                     .filter(CartItem.id == item_id, Cart.user_id == current_user_id)
                     .first())

        if not cart_item:
            return jsonify({"error": "Cart item not found"}), 404

        # Update quantity
        cart_item.quantity = quantity
        cart_item.cart.last_updated_at = db.func.now()

        db.session.commit()

        return jsonify({
            "message": "Cart item updated successfully",
            "cart_item": CartItemSchema().dump(cart_item),
            "cart_total": cart_item.cart.cart_total_value
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to update cart item: {str(e)}"}), 500


# Remove item from cart
@cart_bp.route('/items/<int:item_id>', methods=['DELETE'])
@jwt_required()
def remove_from_cart(item_id):
    """
    Remove a specific item from the cart.
    """
    try:
        current_user_id = int(get_jwt_identity())

        # Find cart item belonging to current user
        cart_item = (db.session.query(CartItem)
                     .join(Cart, CartItem.cart_id == Cart.id)
                     .filter(CartItem.id == item_id, Cart.user_id == current_user_id)
                     .first())

        if not cart_item:
            return jsonify({"error": "Cart item not found"}), 404

        cart = cart_item.cart
        db.session.delete(cart_item)
        cart.last_updated_at = db.func.now()

        db.session.commit()

        return jsonify({
            "message": "Item removed from cart successfully",
            "cart_total": cart.cart_total_value
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to remove item from cart: {str(e)}"}), 500


# Clear entire cart
@cart_bp.route('/clear', methods=['DELETE'])
@jwt_required()
def clear_cart():
    """
    Remove all items from the user's cart.
    """
    try:
        current_user_id = int(get_jwt_identity())

        cart = Cart.query.filter_by(user_id=current_user_id).first()
        if not cart:
            return jsonify({"error": "No active cart found"}), 404

        # Delete all cart items
        CartItem.query.filter_by(cart_id=cart.id).delete()
        cart.last_updated_at = db.func.now()

        db.session.commit()

        return jsonify({"message": "Cart cleared successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to clear cart: {str(e)}"}), 500

# Create cart


@cart_bp.route('/', methods=['POST'])
@jwt_required()
def create_cart():
    try:
        current_user_id = int(get_jwt_identity())

        # Check if user already has an active cart
        existing_cart = Cart.query.filter_by(user_id=current_user_id).first()
        if existing_cart:
            return jsonify({"error": "Active cart already exists"}), 400

        # Create new cart
        new_cart = Cart(user_id=current_user_id)
        db.session.add(new_cart)
        db.session.commit()

        return jsonify(CartSchema().dump(new_cart)), 201

    except Exception as e:
        return jsonify({"error": "Failed to create cart"}), 500

# Get current cart


@cart_bp.route('/', methods=['GET'])
@jwt_required()
def get_cart():
    try:
        current_user_id = int(get_jwt_identity())

        # Retrieve user's active cart
        cart = Cart.query.filter_by(user_id=current_user_id).first()
        if not cart:
            return jsonify({"error": "No active cart found"}), 404

        return jsonify(CartSchema().dump(cart)), 200

    except Exception as e:
        return jsonify({"error": "Failed to fetch cart"}), 500
