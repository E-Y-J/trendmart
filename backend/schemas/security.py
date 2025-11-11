from marshmallow import validate

# Centralized password validator to avoid circular imports
PASSWORD_REGEX = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*(),.?":{}|<>]).+$'
PASSWORD_VALIDATOR = validate.Regexp(
    PASSWORD_REGEX,
    error='Password must include uppercase, lowercase, number, and special character'
)
