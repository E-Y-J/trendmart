from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
import stripe

db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()


class BaseSchema(SQLAlchemyAutoSchema):
    class Meta:
        load_instance = True
        include_fk = True


def init_stripe(app):
    """Initialize Stripe with the application's configuration."""
    stripe.api_key = app.config.get('STRIPE_SECRET_KEY')
    return stripe
