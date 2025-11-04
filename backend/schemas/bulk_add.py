from marshmallow import fields
from extensions import ValidationSchema


class ProductInSchema(ValidationSchema):
    """Lightweight input schema representing a product payload used for bulk/nested creates.

    These are validation-only (no SQLAlchemy model binding) and safe for ingesting
    data structures like Category -> Subcategory -> Product trees.
    """
    id = fields.Int(load_default=None)
    # optional future use if it's added to DB
    external_id = fields.Str(load_default=None)
    sku = fields.Str(load_default=None)
    name = fields.Str(required=True)
    description = fields.Str(load_default="")
    price = fields.Float(load_default=0.0)
    # not stored in DB Product (used for embeddings)
    rating = fields.Float(load_default=0.0)
    tags = fields.List(fields.Str(), load_default=[])
    image_url = fields.Str(load_default=None)
    image_thumb_url = fields.Str(load_default=None)


class SubcategoryInSchema(ValidationSchema):
    '''Lightweight input schema representing a subcategory payload used for bulk/nested creates.'''
    name = fields.Str(required=True)
    products = fields.List(fields.Nested(ProductInSchema), load_default=[])


class CategoryInSchema(ValidationSchema):
    '''Lightweight input schema representing a category payload used for bulk/nested creates.'''
    main_category = fields.Str(required=True)
    subcategories = fields.List(fields.Nested(
        SubcategoryInSchema), load_default=[])


class BulkAddSchema(ValidationSchema):
    '''Top-level schema for bulk adding categories, subcategories, and products.'''
    categories = fields.List(fields.Nested(CategoryInSchema), required=True)
