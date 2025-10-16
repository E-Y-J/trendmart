"""
Product Recommendation Schemas

Marshmallow schemas for ML-generated product recommendations.
Handles personalized product suggestion data for users.

Features:
- Recommendation scoring system
- User-product recommendation mapping
- ML algorithm integration support
- Confidence score validation
"""

from extensions import BaseSchema
from models.recommendation import Recommendation
from marshmallow import fields


class RecommendationSchema(BaseSchema):
    """
    Recommendation Schema for ML-generated product suggestions.

    Handles serialization/deserialization of recommendation data
    including confidence scores and user-product mappings.

    Used for:
    - API responses for personalized product recommendations
    - ML pipeline data output
    - Recommendation engine integration
    """
    class Meta:
        model = Recommendation
        include_fk = True

    user_id = fields.Int(required=True)
    product_id = fields.Int(required=True)
    score = fields.Float(required=True)
