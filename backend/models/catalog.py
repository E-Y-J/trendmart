from extensions import db
from sqlalchemy import CheckConstraint, UniqueConstraint


class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False, index=True)


class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    sku = db.Column(db.String(50), unique=True, nullable=False, index=True)
    name = db.Column(db.String(255), nullable=True, index=True)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    product_img = db.Column(db.String(500))
    times_click_on = db.Column(db.Interger, default=0, nullable=False)
    tags = db.Column(db.String(255))


class Inventory(db.Model):
    __tablename__ = 'inventory'
    product_id = db.Column(
        db.Integer, db.ForeighKey('products.id', ondelte='CASCADE'), primary_key=True)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    restock = db.Column(db.Boolean, default=False, nullable=False)


class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey(
        "products.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False, index=True)
    rating = db.Column(db.Float, nullable=False)
    title = db.Column(db.String(500), nullable=False)
    comment = db.Column(db.Text)
    created_on = db.Column(db.DateTime, default=db.func.now(), nullable=False)

    __table_args__ = (
        CheckConstraint('rating >= 0 AND rating <= 5',
                        name='ck_review_rating_0_5'),
        UniqueConstraint('product_id', 'user_id',
                         name='uq_review_product_user')
    )

    product = db.relationship('Product', back_populates='reviews')
    user = db.relationship('User', back_populates='reviews')
