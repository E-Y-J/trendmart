from marshmallow import fields, validate
from extensions import ValidationSchema


class CategoryInfoInSchema(ValidationSchema):
    main_category = fields.Str(required=True)
    subcategory = fields.Str(required=True)


class ProductFlatInSchema(ValidationSchema):
    """Flat product reference used in user_data ingestion.

    Not nested under categories; includes minimal fields to upsert into catalog
    if missing, leveraging existing bulk add helpers for consistency.
    """
    id = fields.Int(required=True)
    name = fields.Str(required=True)
    description = fields.Str(load_default="")
    price = fields.Float(required=True)
    rating = fields.Float(load_default=0.0)
    tags = fields.List(fields.Str(), load_default=[])
    category_info = fields.Nested(CategoryInfoInSchema, required=True)


class UserInSchema(ValidationSchema):
    user_id = fields.Int(required=True)
    age = fields.Int(load_default=None)
    gender = fields.Str(load_default=None)
    location = fields.Str(load_default=None)
    income_range = fields.Str(load_default=None)
    preferences = fields.List(fields.Str(), load_default=[])
    created_at = fields.Str(load_default=None)


class InteractionInSchema(ValidationSchema):
    user_id = fields.Int(required=True)
    product_id = fields.Int(required=True)
    interaction_type = fields.Str(required=True, validate=validate.OneOf([
        'view', 'add_to_cart', 'rating', 'purchase'
    ]))
    timestamp = fields.Str(required=True)
    duration_seconds = fields.Int(load_default=0)
    rating_given = fields.Float(load_default=None)
    quantity = fields.Int(load_default=None)


class PurchaseInSchema(ValidationSchema):
    user_id = fields.Int(required=True)
    product_id = fields.Int(required=True)
    purchase_date = fields.Str(required=True)
    quantity = fields.Int(required=True)
    price_paid = fields.Float(required=True)
    rating_given = fields.Float(load_default=None)
    review_text = fields.Str(load_default=None)


class SearchQueryInSchema(ValidationSchema):
    user_id = fields.Int(required=True)
    query = fields.Str(required=True)
    timestamp = fields.Str(required=True)
    results_clicked = fields.List(fields.Int(), load_default=[])
    products_purchased = fields.List(fields.Int(), load_default=[])


class SessionInSchema(ValidationSchema):
    session_id = fields.Int(required=True)
    user_id = fields.Int(required=True)
    products_viewed = fields.List(fields.Int(), load_default=[])
    view_durations = fields.List(fields.Int(), load_default=[])
    session_start = fields.Str(required=True)
    session_end = fields.Str(required=True)


class BulkUserDataSchema(ValidationSchema):
    schema_version = fields.Str(load_default=None)
    generated_at = fields.Str(load_default=None)
    products = fields.List(fields.Nested(ProductFlatInSchema), load_default=[])
    users = fields.List(fields.Nested(UserInSchema), load_default=[])
    interactions = fields.List(fields.Nested(
        InteractionInSchema), load_default=[])
    purchases = fields.List(fields.Nested(PurchaseInSchema), load_default=[])
    search_queries = fields.List(fields.Nested(
        SearchQueryInSchema), load_default=[])
    sessions = fields.List(fields.Nested(SessionInSchema), load_default=[])
