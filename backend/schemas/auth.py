from marshmallow import fields, validate
from extensions import BaseSchema
from models.registration import User
from . import PASSWORD_VALIDATOR


class LoginSchema(BaseSchema):
    '''Schema for user login'''
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=PASSWORD_VALIDATOR)


class TokenResponseSchema(BaseSchema):
    '''Schema for token response'''
    access_token = fields.String(required=True, dump_only=True)
    refresh_token = fields.String(required=True, dump_only=True)
    token_type = fields.String(required=True, dump_only=True, default='Bearer')
    # For testing purposes only
    expires_in = fields.Integer(required=True, dump_only=True)


class LogoutSchema(BaseSchema):
    '''Schema for logout response'''
    message = fields.String(dump_only=True, default='Logout successful')
