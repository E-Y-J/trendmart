from flask import Blueprint, request, jsonify
from werkzeug.exceptions import BadRequest
from models.shopping import Order
from utils.payment_service import PaymentService

order_bp = Blueprint("order", __name__, url_prefix="/orders")


@order_bp.route('/<int:order_id>/payments/intents', methods=['POST'])
def order_payment_intent(order_id):
    currency = (request.get_json(silent=True) or {}
                ).get('currency', 'usd').lower()
    order = Order.query.get(order_id)

    if not order:
        raise BadRequest(f'Order {order_id} not found')

    amount_cents = int(round((order_id.total or 0.0) * 100))
    if amount_cents <= 0:
        raise BadRequest('Order total must be greater than zero')

    result = PaymentService.create_payment_intent(
        order_id=order_id,
        amount=amount_cents,
        currency=currency,
        metadata={'source': f'order:{order_id}'}
    )

    return jsonify(result), 201
