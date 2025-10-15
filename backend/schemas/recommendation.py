from extentions import BaseSchema
from models.recommendation import Recommendation, Reviews
from marshmallow import fields


class RecommendationSchema(BaseSchema):
    class Meta:
        model = Recommendation
        include_fk = True


class ReviewsSchema(BaseSchema):
    class Meta:
        model = Reviews
        include_fk = True
    product_id = fields.Int(required=True)
