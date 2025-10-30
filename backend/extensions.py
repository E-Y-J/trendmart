from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import Schema
import stripe

db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()
jwt = JWTManager()
cors = CORS()


class BaseSchema(SQLAlchemyAutoSchema):
    class Meta:
        load_instance = True
        include_fk = True

class ValidationSchema(Schema):
    """Base schema for validation only (no model instances)"""
    pass


def init_stripe(app):
    """Initialize Stripe with the application's configuration."""
    stripe.api_key = app.config.get('STRIPE_SECRET_KEY')
    return stripe
