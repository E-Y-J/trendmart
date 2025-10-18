from .catalog import *
from .registration import *
from .shopping import *
from .auth import *
from .payment import *
from .recommendation import *
from marshmallow import validate

PASSWORD_REGEX = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*(),.?":{}|<>]).+$'
PASSWORD_VALIDATOR = validate.Regexp(
    PASSWORD_REGEX,
    error='Password must include uppercase, lowercase, number, and special character'
)


__all__ = [
    'PASSWORD_VALIDATOR'
]
