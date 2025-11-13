from extensions import db
from datetime import datetime


class ProductInteraction(db.Model):
    """Atomic product interaction events (duplicate definition kept for legacy imports).

    Note: This mirrors models.recommendation_feedback.ProductInteraction.
    Prefer importing from models.recommendation_feedback going forward.
    """
    __tablename__ = 'product_interactions'

    id = db.Column(db.Integer, primary_key=True)
    # user_id is optional; anonymous events are allowed
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    product_id = db.Column(db.Integer, db.ForeignKey(
        'products.id'), nullable=False)
    event_type = db.Column(db.String(32), nullable=False, index=True)
    # search|similar|related|answer|cold_start
    source = db.Column(db.String(32), nullable=True)
    session_id = db.Column(db.Integer, db.ForeignKey(
        'user_sessions.id'), nullable=True)
    context_json = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=db.func.now(), nullable=False)

    # Align index naming and fields with primary model
    __table_args__ = (
        db.Index("ix_product_interactions_prod_evt",
                 "product_id", "event_type"),
    )


class RecommendationFeedback(db.Model):
    """Aggregated feedback specific to recommendation quality (legacy duplicate).

    Prefer importing from models.recommendation_feedback.RecommendationFeedback.
    """
    __tablename__ = 'recommendation_feedback'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    product_id = db.Column(db.Integer, db.ForeignKey(
        'products.id'), nullable=False)
    # search|similar|related|answer|cold_start
    source = db.Column(db.String(32), nullable=False)
    # e.g., 'click', 'add_to_cart', 'purchase'
    action = db.Column(db.String(32), nullable=False)
    # Change in recommendation score
    score_delta = db.Column(db.Float, nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.now(), nullable=False)

    __table_args__ = (
        db.Index("ix_recom_feedback_prod_src", "product_id", "source"),
        db.Index("ix_recom_feedback_user_prod", "user_id", "product_id"),
    )
