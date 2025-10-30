from marshmallow import fields, validate
from extensions import ValidationSchema
from models.registration import User
from . import PASSWORD_VALIDATOR


class LoginSchema(ValidationSchema):
    """
    User Login Schema

    Validates login credentials with security best practices.
    - Email format validation
    - Password complexity requirements
    """
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=PASSWORD_VALIDATOR)


class TokenResponseSchema(ValidationSchema):
    """
    JWT Token Response Schema

    Standardized format for authentication token responses.
    All fields are dump-only (output only) for security.
    """
    access_token = fields.String(
        required=True, dump_only=True)
    refresh_token = fields.String(
        required=True, dump_only=True)
    token_type = fields.String(
        # required=True, dump_only=True, default='Bearer')
        required=True, dump_only=True)
    # Token lifetime in seconds for testing purposes
    expires_in = fields.Integer(required=True, dump_only=True)


class LogoutSchema(ValidationSchema):
    """
    Logout Response Schema

    Simple success message for logout operations.
    """
    # message = fields.String(dump_only=True, default='Logout successful')
    message = fields.String(dump_only=True)
