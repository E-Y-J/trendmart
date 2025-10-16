from marshmallow import Schema, fields, validate, validates, ValidationError
from extensions import BaseSchema
from models.catalog import Product, Category, Inventory, Review

# -------Read and Write Schemas------- #


class CategorySchema(BaseSchema):
    """
    Category Schema for API serialization/deserialization.
    Automatically includes all Category model fields.
    """
    class Meta:
        model = Category


class ProductSchema(BaseSchema):
    """
    Product Schema for API responses.
    Includes nested category and review data for complete product information.
    """
    class Meta:
        model = Product

    # Nested relationships for rich API responses (read-only)
    categories = fields.Nested(CategorySchema, many=True, dump_only=True)
    reviews = fields.Nested('ReviewSchema', many=True, dump_only=True)


class InventorySchema(BaseSchema):
    """
    Inventory Schema for stock management API operations.
    Handles product inventory tracking and restock flags.
    """
    class Meta:
        model = Inventory


class ReviewSchema(BaseSchema):
    """
    Review Schema with custom validation for rating field.
    Enforces business rule: ratings must be between 0-5.
    """
    class Meta:
        model = Review

    # Custom validation for rating field (supplements database constraint)
    @validates('rating')
    def validate_rating(self, value):
        """Ensure rating is within valid range (0-5 stars)"""
        if value < 0 or value > 5:
            raise ValidationError('Rating must be between 0 and 5')

# -------Input Schemas------- #


class ProductCreateSchema(BaseSchema):
    """
    Product Creation Schema with validation rules.

    Excludes auto-generated fields and provides category assignment via IDs.
    Implements business validation rules for product data integrity.
    """
    class Meta:
        model = Product
        # Exclude auto/relationship fields
        exclude = ('id', 'categories', 'reviews')

    # Category assignment via ID list (converted to relationships in business logic)
    category_ids = fields.List(fields.Integer(), load_only=True)
    price = fields.Float(required=True, validate=validate.Range(min=0))
    name = fields.String(required=True, validate=validate.Length(min=1))
    sku = fields.String(required=True, validate=validate.Length(min=1))
    description = fields.String(validate=validate.Length(min=1))
    product_img = fields.String(validate=validate.Length(min=1))
    tags = fields.String(validate=validate.Length(min=1))


class ProductUpdateSchema(ProductCreateSchema):
    """
    Product Update Schema - inherits all validation from ProductCreateSchema.
    Same validation rules apply for updates as creates.
    """
    pass
