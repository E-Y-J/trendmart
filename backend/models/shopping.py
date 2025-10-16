from extensions import db
from sqlalchemy import UniqueConstraint


class Cart(db.Model):
    """
    Shopping Cart Model

    Represents a user's active shopping cart.
    Each user has exactly one cart that persists between sessions.

    Attributes:
        id (int): Primary key, unique cart identifier
        user_id (int): Foreign key to User, unique (one cart per user)

    Business Rules:
        - One cart per user (enforced by unique constraint)
        - Cart persists until explicitly cleared or converted to order
        - Items cascade delete when cart is deleted
    """
    __tablename__ = 'carts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id', ondelete='CASCADE'), nullable=False, unique=True)

    # Relationships
    user = db.relationship('User', back_populates='cart')
    # One-to-many: cart can contain multiple items
    items = db.relationship('CartItem', back_populates='cart',
                            cascade='all, delete-orphan')


class CartItem(db.Model):
    """
    Cart Item Model

    Represents individual products within a shopping cart.
    Links products to carts with quantity and pricing information.

    Attributes:
        id (int): Primary key, unique cart item identifier
        cart_id (int): Foreign key to Cart this item belongs to
        product_id (int): Foreign key to Product being purchased
        quantity (int): Number of units in cart, defaults to 1
        price_per_unit (float): Price snapshot when item was added

    Business Rules:
        - One entry per product per cart (enforced by unique constraint)
        - Price captured when item added (protects against price changes)
        - Quantity must be positive (should be validated at application level)
    """
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

    # Relationships
    cart = db.relationship('Cart', back_populates='items')
    product = db.relationship('Product', back_populates='cart_items')


class Order(db.Model):
    """
    Order Model

    Represents a completed purchase order (converted from cart).
    Contains pricing snapshot and order status for fulfillment tracking.

    Attributes:
        id (int): Primary key, unique order identifier
        user_id (int): Foreign key to User (nullable for guest orders)
        status (str): Order status (pending, processing, shipped, delivered, etc.)
        subtotal (float): Sum of all items before taxes and fees
        tax_total (float): Total tax amount calculated at order time
        total (float): Final total including all charges
        placed_at (datetime): Timestamp when order was placed

    Business Rules:
        - User can be null (allows guest checkout and account deletion)
        - Pricing frozen at order time (immutable historical record)
        - Status tracks order through fulfillment pipeline
    """
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id', ondelete='SET NULL'), nullable=True)
    status = db.Column(db.String(32), nullable=False, default='pending')
    subtotal = db.Column(db.Float, nullable=False)
    tax_total = db.Column(db.Float, nullable=False)
    total = db.Column(db.Float, nullable=False)
    placed_at = db.Column(db.DateTime, default=db.func.now(), nullable=False)

    # Relationships
    user = db.relationship('User', back_populates='orders')
    # One-to-many: order contains multiple items
    items = db.relationship(
        'OrderItem', back_populates='order', cascade='all, delete-orphan')
    # One-to-one: each order has one payment record
    payment = db.relationship(
        'Payment', back_populates='order', uselist=False, cascade='all, delete-orphan')


class OrderItem(db.Model):
    """
    Order Item Model

    Represents individual products within a completed order.
    Immutable historical record of what was purchased and at what price.

    Attributes:
        id (int): Primary key, unique order item identifier
        order_id (int): Foreign key to Order this item belongs to
        product_id (int): Foreign key to Product (nullable for deleted products)
        quantity (int): Number of units purchased
        price_per_unit (float): Historical price when order was placed

    Business Rules:
        - Immutable once order is placed (historical record)
        - Product reference nullable (allows product deletion while preserving order history)
        - Price snapshot preserves historical pricing for accounting
    """
    __tablename__ = 'order_items'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey(
        'orders.id', ondelete='CASCADE'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey(
        'products.id', ondelete='SET NULL'), nullable=True)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    price_per_unit = db.Column(db.Float, nullable=False)

    # Relationships
    order = db.relationship('Order', back_populates='items')
    product = db.relationship('Product', back_populates='order_items')
