from marshmallow import fields
from extensions import BaseSchema
from models.payment import Payment

# -------Read and Write Schemas------- #


class PaymentSchema(BaseSchema):
    '''Schema for reading and writing Payment data'''
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

# -------Input Schemas------- #


class PaymentCreateSchema(BaseSchema):
    '''Schema for creating a new Payment'''
    class Meta:
        model = Payment
        exclude = ('id', 'created_at', 'updated_at', 'status', 'paid_at')

    order_id = fields.Int(required=True)
    total_amount = fields.Float(required=True, validate=lambda p: p >= 0)
    currency = fields.Str(required=True)
    payment_method = fields.Str(required=True)
    stripe_payment_intent_id = fields.Str()


class PaymentUpdateSchema(BaseSchema):
    '''Schema for updating Payment status'''
    class Meta:
        model = Payment
        exclude = ('id', 'created_at', 'order_id', 'total_amount',
                   'currency', 'payment_method', 'paid_at')

    status = fields.Str(required=True)
    updated_at = fields.DateTime(dump_only=True)


# -------Container Class------- #


class PaymentSchemas:
    """Container class for all payment schemas"""

    # Read/Write schemas
    PaymentSchema = PaymentSchema

    # Input schemas
    PaymentCreateSchema = PaymentCreateSchema
    PaymentUpdateSchema = PaymentUpdateSchema
