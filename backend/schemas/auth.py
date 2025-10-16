"""
Authentication Schemas

Marshmallow schemas for user authentication endpoints.
Handles login/logout request validation and JWT token responses.

Security Features:
- Password complexity validation via regex
- Email format validation
- Token response standardization
"""

from marshmallow import fields, validate
from extensions import BaseSchema
from models.registration import User
from . import PASSWORD_VALIDATOR


class LoginSchema(BaseSchema):
    """
    User Login Schema

    Validates login credentials with security best practices.
    - Email format validation
    - Password complexity requirements
    """
    email = fields.Email(required=True)  # Built-in email format validation
    # Complex password required
    password = fields.String(required=True, validate=PASSWORD_VALIDATOR)


class TokenResponseSchema(BaseSchema):
    """
    JWT Token Response Schema

    Standardized format for authentication token responses.
    All fields are dump-only (output only) for security.
    """
    access_token = fields.String(
        required=True, dump_only=True)   # JWT access token
    refresh_token = fields.String(
        required=True, dump_only=True)  # JWT refresh token
    token_type = fields.String(
        required=True, dump_only=True, default='Bearer')  # Token type
    # Token lifetime in seconds
    expires_in = fields.Integer(required=True, dump_only=True)


class LogoutSchema(BaseSchema):
    """
    Logout Response Schema

    Simple success message for logout operations.
    """
    message = fields.String(dump_only=True, default='Logout successful')
