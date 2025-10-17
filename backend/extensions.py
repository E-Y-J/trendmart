from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
import stripe

db = SQLAlchemy()
migrate = Migrate()


class BaseSchema(SQLAlchemyAutoSchema):
    class Meta:
        load_instance = True
        include_fk = True


def init_stripe(app):
    """Initialize Stripe with the application's configuration."""
    stripe.api_key = app.config.get('STRIPE_SECRET_KEY')
    return stripe
