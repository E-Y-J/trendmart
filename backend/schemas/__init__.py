from marshmallow import validate

# Define PASSWORD_VALIDATOR first to avoid circular imports
PASSWORD_REGEX = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*(),.?":{}|<>]).+$'
PASSWORD_VALIDATOR = validate.Regexp(
    PASSWORD_REGEX,
    error="Password must include uppercase, lowercase, number, and special character",
)

from .registration import *
from .auth import *
from .catalog import *
from .shopping import *
from .payment import *
from .recommendation import *

__all__ = ["PASSWORD_VALIDATOR"]
