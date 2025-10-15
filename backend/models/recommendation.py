from extentions import BaseSchema
from sqlalchemy import UniqueConstraint


class Recommendation(db.Model):
    __tablename__ = 'recommendations'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id'), ondelete='CASCADE', nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey(
        'products.id'), ondelete='CASCADE', nullable=False, index=True)
