from marshmallow import fields
from extensions import BaseSchema
from models.shopping import Cart, CartItem, Order, OrderItem

# -------Read and Write Schemas------- #


class CartItemSchema(BaseSchema):
    '''Schema for reading and writing CartItem data'''
    class Meta:
        model = CartItem
        include_fk = True
    product_id = fields.Int(required=True)
    quantity = fields.Int(required=True, validate=lambda n: n > 0)


class CartSchema(BaseSchema):
    '''Schema for reading and writing Cart data'''
    class Meta:
        model = Cart
        include_fk = True
    items = fields.Nested(CartItemSchema, many=True, dump_only=True)
    user_id = fields.Int(required=True)


class OrderItemSchema(BaseSchema):
    '''Schema for reading and writing OrderItem data'''
    class Meta:
        model = OrderItem
        include_fk = True
    product_id = fields.Int(required=True)
    quantity = fields.Int(required=True)
    price = fields.Float(required=True)


class OrderSchema(BaseSchema):
    '''Schema for reading and writing Order data'''
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


# -------Input Schemas------- #


class CartCreateSchema(BaseSchema):
    '''Schema for creating a new Cart'''
    class Meta:
        model = Cart
        exclude = ('id', 'created_at', 'updated_at', 'items')
    user_id = fields.Int(required=True)


class CartItemCreateSchema(BaseSchema):
    '''Schema for creating a new CartItem'''
    class Meta:
        model = CartItem
        exclude = ('id', 'cart_id', 'created_at', 'updated_at')
    product_id = fields.Int(required=True)
    quantity = fields.Int(required=True, validate=lambda n: n > 0)
    price_per_unit = fields.Float(required=True, validate=lambda p: p >= 0)


class OrderCreateSchema(BaseSchema):
    '''Schema for creating a new Order'''
    class Meta:
        model = Order
        exclude = ('id', 'created_at', 'updated_at', 'status',
                   'subtotal', 'tax_total', 'total', 'placed_at', 'items')
    user_id = fields.Int(required=True)


class OrderItemCreateSchema(BaseSchema):
    '''Schema for creating a new OrderItem'''
    class Meta:
        model = OrderItem
        exclude = ('id', 'order_id', 'created_at', 'updated_at')
    product_id = fields.Int(required=True)
    quantity = fields.Int(required=True, validate=lambda n: n > 0)
    price_per_unit = fields.Float(required=True, validate=lambda p: p >= 0)
