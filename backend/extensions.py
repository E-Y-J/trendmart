from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import Schema
import stripe

db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()
jwt = JWTManager()


class BaseSchema(SQLAlchemyAutoSchema):
    class Meta:
        load_instance = True
        include_fk = True
        sqla_session = db.session


class ValidationSchema(Schema):
    """Base schema for validation only (no model instances)"""
    pass


def init_stripe(app):
    """Initialize Stripe with the application's configuration."""
    stripe.api_key = app.config.get('STRIPE_SECRET_KEY')
    return stripe
