from extensions import db
from datetime import datetime


class ProductInteraction(db.Model):
    ''' Model to log user interactions with products for recommendation feedback

    event_types:
        - view: User viewed a product
        - click: User clicked on a product
        - add_to_cart: User added a product to their cart
        - purchase: User purchased a product
    '''
    __tablename__ = 'product_interactions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey(
        'products.id'), nullable=False)
    event_type = db.Column(db.String(50), nullable=False, index=True)
    source = db.Column(db.String(100), nullable=True)
    session_id = db.Column(db.Integer, db.ForeignKey(
        'user_sessions.id'), nullable=True)
    context_json = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=db.func.now(), nullable=False)

    # Simple index to optimize common queries filtering by user, product, and event type
    __table_args__ = (
        db.Index('ix_product_interactions_user_product_event',
                 'user_id', 'product_id', 'event_type'),
    )


class RecommendationFeedback(db.Model):
    __tablename__ = 'recommendation_feedback'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey(
        'products.id'), nullable=False)
    source = db.Column(db.String(100), nullable=True)
    # e.g., 'click', 'add_to_cart', 'purchase'
    action = db.Column(db.String(50), nullable=False, index=True)
    # Change in recommendation score
    score_delta = db.Column(db.Float, nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.now(), nullable=False)

    __table_args__ = (
        db.Index("ix_recom_feedback_prod_src", "product_id", "source"),
        db.Index("ix_recom_feedback_user_prod", "user_id", "product_id"),
    )
