from .bulk_add import *
from .recommendation import *
from .payment import *
from .shopping import *
from .catalog import *
from .auth import *
from .registration import *
from marshmallow import validate

# Define PASSWORD_VALIDATOR first to avoid circular imports
PASSWORD_REGEX = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*(),.?":{}|<>]).+$'
PASSWORD_VALIDATOR = validate.Regexp(
    PASSWORD_REGEX,
    error='Password must include uppercase, lowercase, number, and special character'
)


__all__ = [
    'PASSWORD_VALIDATOR'
]
