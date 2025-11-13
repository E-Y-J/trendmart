from marshmallow import fields, validates, ValidationError
from extensions import ValidationSchema

VALID_INTERACTION_EVENTS = {"view", "click",
                            "add_to_cart", "purchase", "dismiss"}
VALID_FEEDBACK_ACTIONS = {"clicked", "converted",
                          "ignored", "dismissed", "pinned"}
VALID_SOURCES = {"search", "similar", "related", "answer", "cold_start"}


class ProductInteractionCreateSchema(ValidationSchema):
    user_id = fields.Int(load_default=None)
    product_id = fields.Int(required=True)
    event_type = fields.Str(required=True)
    source = fields.Str(load_default=None)
    session_id = fields.Int(load_default=None)
    context_json = fields.Dict(load_default=None)

    @validates("event_type")
    def _validate_event_type(self, value, **kwargs):
        if value not in VALID_INTERACTION_EVENTS:
            raise ValidationError(
                f"event_type must be one of {sorted(VALID_INTERACTION_EVENTS)}")

    @validates("source")
    def _validate_source(self, value, **kwargs):
        if value and value not in VALID_SOURCES:
            raise ValidationError(
                f"source must be one of {sorted(VALID_SOURCES)}")


class RecommendationFeedbackCreateSchema(ValidationSchema):
    user_id = fields.Int(load_default=None)
    product_id = fields.Int(required=True)
    source = fields.Str(required=True)
    action = fields.Str(required=True)
    score_delta = fields.Float(load_default=None)

    @validates("source")
    def _validate_source(self, value, **kwargs):
        if value not in VALID_SOURCES:
            raise ValidationError(
                f"source must be one of {sorted(VALID_SOURCES)}")

    @validates("action")
    def _validate_action(self, value, **kwargs):
        if value not in VALID_FEEDBACK_ACTIONS:
            raise ValidationError(
                f"action must be one of {sorted(VALID_FEEDBACK_ACTIONS)}")
