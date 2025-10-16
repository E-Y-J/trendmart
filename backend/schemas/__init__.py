from catalog import CatalogSchemas
from registration import RegistrationSchemas
from shopping import ShoppingSchemas
from auth import AuthSchemas
from marshmallow import validate

PASSWORD_REGEX = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*(),.?":{}|<>]).+$'
PASSWORD_VALIDATOR = validate.Regexp(
    PASSWORD_REGEX,
    error='Password must include uppercase, lowercase, number, and special character'
)


__all__ = [
    'CatalogSchemas',
    'RegistrationSchemas',
    'ShoppingSchemas',
    'AuthSchemas',
    'PASSWORD_VALIDATOR'
]
