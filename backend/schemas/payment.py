from marshmallow import fields
from extensions import BaseSchema
from models.payment import Payment


class PaymentSchema(BaseSchema):
    """
    Payment Schema for API serialization/deserialization.

    Used for reading payment data and API responses.
    Includes all payment fields with proper validation.
    """
    class Meta:
        model = Payment
        include_fk = True

    order_id = fields.Int(required=True)
    total_amount = fields.Float(required=True)
    currency = fields.Str(required=True)
    payment_method = fields.Str(required=True)
    status = fields.Str(dump_only=True)
    paid_at = fields.DateTime(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class PaymentCreateSchema(BaseSchema):
    """
    Payment Creation Schema with validation rules.

    Used for creating new payment records with business validation.
    Excludes auto-generated fields and enforces payment amount validation.

    Validation Rules:
    - Total amount must be non-negative
    - Required fields: order_id, total_amount, currency, payment_method
    - Optional: stripe_payment_intent_id for processor integration
    """
    class Meta:
        model = Payment
        exclude = ('id', 'created_at', 'updated_at', 'status', 'paid_at')

    order_id = fields.Int(required=True)
    total_amount = fields.Float(required=True, validate=lambda p: p >= 0)
    currency = fields.Str(required=True)
    payment_method = fields.Str(required=True)
    stripe_payment_intent_id = fields.Str()


class PaymentUpdateSchema(BaseSchema):
    """
    Payment Status Update Schema.

    Used for updating payment status after processing.
    Only allows status updates, excludes financial data for security.

    Use Cases:
    - Mark payment as completed after successful processing
    - Update status to failed for declined transactions
    - Set status to refunded for refund processing
    """
    class Meta:
        model = Payment
        exclude = ('id', 'created_at', 'order_id', 'total_amount',
                   'currency', 'payment_method', 'paid_at')

    status = fields.Str(required=True)
    updated_at = fields.DateTime(dump_only=True)


class PaymentSchemas:
    """Container class for all payment schemas"""

    PaymentSchema = PaymentSchema
    PaymentCreateSchema = PaymentCreateSchema
    PaymentUpdateSchema = PaymentUpdateSchema
