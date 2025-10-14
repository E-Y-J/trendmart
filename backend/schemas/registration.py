from marshmallow import fields
from extensions import BaseSchema
from models.registration import User, CustomerProfile, Address

# -------Read and Write Schemas------- #


class AddressSchema(BaseSchema):
    class Meta:
        model = Address


class CustomerProfileSchema(BaseSchema):
    class Meta:
        model = CustomerProfile

    default_address = fields.Nested(AddressSchema, dump_only=True)


class UserSchema(BaseSchema):
    class Meta:
        model = User
        exclude = ("password_hash",)

    customer_profile = fields.Nested(CustomerProfileSchema, dump_only=True)
    addresses = fields.Nested(AddressSchema, many=True, dump_only=True)
