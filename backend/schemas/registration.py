from wsgiref import validate
from marshmallow import fields
from extensions import BaseSchema
from models.registration import User, CustomerProfile, Address
from __init__ import PASSWORD_VALIDATOR

# -------Read and Write Schemas------- #


class AddressSchema(BaseSchema):
    '''Schema for reading and writing Address data'''
    class Meta:
        model = Address


class CustomerProfileSchema(BaseSchema):
    '''Schema for reading and writing CustomerProfile data'''
    class Meta:
        model = CustomerProfile

    default_address = fields.Nested(AddressSchema, dump_only=True)


class UserSchema(BaseSchema):
    '''Schema for reading and writing User data'''
    class Meta:
        model = User
        exclude = ("password_hash",)

    customer_profile = fields.Nested(CustomerProfileSchema, dump_only=True)
    addresses = fields.Nested(AddressSchema, many=True, dump_only=True)

# -------Input Schemas------- #


class UserRegistrationSchema(BaseSchema):
    '''Schema for registering a new User'''
    class Meta:
        model = User
        exclude = ('id', 'created_at', 'active', 'role',
                   'customer profile', 'addresses')

    password = fields.String(
        required=True,
        validate=[
            validate.Length(min=8, max=50),
            PASSWORD_VALIDATOR
        ]
    )
    role = fields.String(dump_only=True, default='customer')
    email = fields.Email(required=True)


class CustomerProfileInputSchema(BaseSchema):
    '''Schema for creating or updating CustomerProfile data'''
    class Meta:
        model = CustomerProfile
        exclude = ('id', 'user_id', 'default_address', 'user', 'addresses')
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
