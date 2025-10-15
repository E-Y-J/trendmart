from sqlalchemy import CheckConstraint, UniqueConstraint
from extensions import db


class Recommendation(db.Model):
    __tablename__ = 'recommendations'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id'), ondelete='CASCADE', nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey(
        'products.id'), ondelete='CASCADE', nullable=False, index=True)
    score = db.Column(db.Float, nullable=False, default=0.0)
    generated_on = db.Column(
        db.DateTime, default=db.func.now(), nullable=False)

    __table_args__ = (UniqueConstraint(
        'user_id', 'product_id', name='uq_recommendation_user_product'),)

    user = db.relationship('User', back_populates='recommendations')
    product = db.relationship('Product', back_populates='recommendations')


class Reviews(db.Model):
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
