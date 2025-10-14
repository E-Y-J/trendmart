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
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE')
