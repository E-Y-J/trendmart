from extensions import db
from sqlalchemy import UniqueConstraint


class Cart(db.Model):
    __tablename__ = 'carts'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id', ondelete='CASCADE'), nullable=False, unique=True)

    user = db.relationship('User', back_populates='cart')
    items = db.relationship('CartItem', back_populates='cart',
                            cascade='all, delete-orphan')


class CartItem(db.Model):
    __tablename__ = 'cart_items'

    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey(
        'carts.id', ondelete='CASCADE'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey(
        'products.id', ondelete='CASCADE'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    price_per_unit = db.Column(db.Float, nullable=False)

    __table_args__ = (UniqueConstraint(
        'cart_id', 'product_id', name='uq_cartitem_cart_product'),)

    cart = db.relationship('Cart', back_populates='items')
    product = db.relationship('Product', back_populates='cart_items')


class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id', ondelete='SET NULL'), nullable=True)
    status = db.Column(db.String(32), nullable=False, default='pending')
    subtotal = db.Column(db.Float, nullable=False)
    tax_total = db.Column(db.Float, nullable=False)
    total = db.Column(db.Float, nullable=False)
    placed_at = db.Column(db.DateTime, default=db.func.now(), nullable=False)

    user = db.relationship('User', back_populates='orders')
    items = db.relationship(
        'OrderItem', back_populates='order', cascade='all, delete-orphan')
    payment = db.relationship(
        'Payment', back_populates='order', uselist=False, cascade='all, delete-orphan')


class OrderItem(db.Model):
    __tablename__ = 'order_items'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey(
        'orders.id', ondelete='CASCADE'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey(
        'products.id', ondelete='SET NULL'), nullable=True)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    price_per_unit = db.Column(db.Float, nullable=False)

    order = db.relationship('Order', back_populates='items')
    product = db.relationship('Product', back_populates='order_items')


class Payment(db.Model):
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey(
        'orders.id', ondelete='CASCADE'), nullable=False, unique=True)
    status = db.Column(db.String(32), nullable=False, default='pending')
    total_amount = db.Column(db.Float, nullable=False)
    paid_at = db.Column(db.DateTime)

    order = db.relationship('Order', back_populates='payment')
