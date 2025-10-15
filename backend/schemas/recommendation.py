from extentions import BaseSchema
from models.recommendation import Recommendation, Reviews


class RecommendationSchema(BaseSchema):
    class Meta:
        model = Recommendation


class ReviewsSchema(BaseSchema):
    class Meta:
        model = Reviews
