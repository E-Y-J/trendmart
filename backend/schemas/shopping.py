from marshmallow import fields
from extensions import BaseSchema
from models.shopping import Cart, CartItem, Order, OrderItem, Payment

# -------Read and Write Schemas------- #


class CartItemSchema(BaseSchema):
    class Meta:
        model = CartItem
        include_fk = True
    product_id = fields.Int(required=True)
    quantity = fields.Int(required=True, validate=lambda n: n > 0)


class CartSchema(BaseSchema):
    class Meta:
        model = Cart
        include_fk = True
    items = fields.Nested(CartItemSchema, many=True, dump_only=True)
    user_id = fields.Int(required=True)


class OrderItemSchema(BaseSchema):
    class Meta:
        model = OrderItem
        include_fk = True
    product_id = fields.Int(required=True)
    quantity = fields.Int(required=True)
    price = fields.Float(required=True)


class OrderSchema(BaseSchema):
    class Meta:
        model = Order
        include_fk = True
    items = fields.Nested(OrderItemSchema, many=True, dump_only=True)
    user_id = fields.Int(required=True)
    status = fields.Str(dump_only=True)
    subtotal = fields.Float(dump_only=True)
    tax_total = fields.Float(dump_only=True)
    total = fields.Float(dump_only=True)
    placed_at = fields.DateTime(dump_only=True)


class PaymentSchema(BaseSchema):
    class Meta:
        model = Payment
        include_fk = True
    order_id = fields.Int(required=True)
    amount = fields.Float(required=True)
    currency = fields.Str(required=True)
    payment_method = fields.Str(required=True)
    status = fields.Str(dump_only=True)
    paid_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

# -------Input Schemas------- #


class CartCreateSchema(BaseSchema):
    class Meta:
        model = Cart
        exclude = ('id', 'created_at', 'updated_at', 'items')
    user_id = fields.Int(required=True)


class CartItemCreateSchema(BaseSchema):
    class Meta:
        model = CartItem
        exclude = ('id', 'cart_id', 'created_at', 'updated_at')
    product_id = fields.Int(required=True)
    quantity = fields.Int(required=True, validate=lambda n: n > 0)
    price_per_unit = fields.Float(required=True, validate=lambda p: p >= 0)


class OrderCreateSchema(BaseSchema):
    class Meta:
        model = Order
        exclude = ('id', 'created_at', 'updated_at', 'status',
                   'subtotal', 'tax_total', 'total', 'placed_at', 'items')
    user_id = fields.Int(required=True)


class OrderItemCreateSchema(BaseSchema):
    class Meta:
        model = OrderItem
        exclude = ('id', 'order_id', 'created_at', 'updated_at')
    product_id = fields.Int(required=True)
    quantity = fields.Int(required=True, validate=lambda n: n > 0)
    price_per_unit = fields.Float(required=True, validate=lambda p: p >= 0)


class PaymentCreateSchema(BaseSchema):
    class Meta:
        model = Payment
        exclude = ('id', 'created_at', 'updated_at', 'status', 'paid_at')
    order_id = fields.Int(required=True)
    total_amount = fields.Float(required=True, validate=lambda p: p >= 0)
    currency = fields.Str(required=True)
    payment_method = fields.Str(required=True)
    stripe_payment_intent_id = fields.Str()


class PaymentUpdateSchema(BaseSchema):
    class Meta:
        model = Payment
        exclude = ('id', 'created_at', 'order_id', 'total_amount',
                   'currency', 'payment_method', 'paid_at')
    status = fields.Str(required=True)
    updated_at = fields.DateTime(dump_only=True)
