from extensions import db


class ProductInteraction(db.Model):
    """
    Atomic product interaction events.

    event_type:
      - view        (card or PDP view)
      - click       (card/product click)
      - add_to_cart
      - purchase
      - dismiss     (user hides/ignores a recommendation)
    """
    __tablename__ = "product_interactions"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    product_id = db.Column(db.Integer, db.ForeignKey(
        "products.id"), nullable=False)
    event_type = db.Column(db.String(32), nullable=False, index=True)
    # search|similar|related|answer|cold_start
    source = db.Column(db.String(32), nullable=True)
    session_id = db.Column(db.Integer, db.ForeignKey(
        "user_sessions.id"), nullable=True)
    context_json = db.Column(db.Text)  # optional JSON string
    created_at = db.Column(db.DateTime, default=db.func.now(), nullable=False)

    __table_args__ = (
        db.Index("ix_product_interactions_prod_evt",
                 "product_id", "event_type"),
    )


class RecommendationFeedback(db.Model):
    """
    Aggregated feedback specific to recommendation quality.

    action:
      - clicked
      - converted
      - ignored
      - dismissed
      - pinned
    """
    __tablename__ = "recommendation_feedback"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    product_id = db.Column(db.Integer, db.ForeignKey(
        "products.id"), nullable=False)
    # search|similar|related|answer|cold_start
    source = db.Column(db.String(32), nullable=False)
    action = db.Column(db.String(32), nullable=False)
    score_delta = db.Column(db.Float, nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.now(), nullable=False)

    __table_args__ = (
        db.Index("ix_recom_feedback_prod_src", "product_id", "source"),
        db.Index("ix_recom_feedback_user_prod", "user_id", "product_id"),
    )
