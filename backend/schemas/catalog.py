from marshmallow import Schema, fields, validate, validates, ValidationError
from extensions import BaseSchema
from models.catalog import Product, Category, Inventory, Review

# -------Read and Write Schemas------- #


class CategorySchema(BaseSchema):
    class Meta:
        model = Category


class ProductSchema(BaseSchema):
    class Meta:
        model = Product

    categories = fields.Nested(CategorySchema, many=True, dump_only=True)
    reviews = fields.Nested('ReviewSchema', many=True, dump_only=True)


class InventorySchema(BaseSchema):
    class Meta:
        model = Inventory


class ReviewSchema(BaseSchema):
    class Meta:
        model = Review

    # validates rating to be between 0 and 5
    @validates('rating')
    def validate_rating(self, value):
        if value < 0 or value > 5:
            raise ValidationError('Rating must be between 0 and 5')

# -------Input Schemas------- #


class ProductCreateSchema(BaseSchema):
    class Meta:
        model = Product
        exclude = ('id', 'categories', 'reviews')

    category_ids = fields.List(fields.Integer(), load_only=True)
    price = fields.Float(required=True, validate=validate.Range(min=0))
    name = fields.String(required=True, validate=validate.Length(min=1))
    description = fields.String(validate=validate.Length(min=1))
    sku = fields.String(required=True, validate=validate.Length(min=1))
    product_img = fields.String(validate=validate.Length(min=1))
    tags = fields.String(validate=validate.Length(min=1))


class ProductUpdateSchema(ProductCreateSchema):
    pass
