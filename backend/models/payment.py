from extensions import db


class Payment(db.Model):
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey(
        'orders.id', ondelete='CASCADE'), nullable=False, unique=True)
    status = db.Column(db.String(32), nullable=False, default='pending')
    total_amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(10), nullable=False, default='USD')
    payment_method = db.Column(db.String(50), nullable=False)
    stripe_payment_intent_id = db.Column(db.String(255), unique=True)
    paid_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=db.func.now(), nullable=False)
    updated_at = db.Column(db.DateTime, default=db.func.now(),
                           onupdate=db.func.now(), nullable=False)

    order = db.relationship('Order', back_populates='payment')
