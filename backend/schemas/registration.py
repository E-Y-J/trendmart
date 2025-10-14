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

# -------Input Schemas------- #


class UserRegistrationSchema(BaseSchema):
    class Meta:
        model = User
        exclude = ('id', 'created_at', 'active', 'role',
                   'customer profile', 'addresses')

    password = fields.String(load_only=True, required=True)
    role = fields.String(dump_only=True, default='customer')
    email = fields.Email(required=True)


class CustomerProfileInputSchema(BaseSchema):
    class Meta:
        model = CustomerProfile
        exclude = ('id', 'user_id', 'default_address', 'user', 'addresses')
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
