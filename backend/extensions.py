from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from marshmallow import Schema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

db = SQLAlchemy()
migrate = Migrate()


class BaseSchema(SQLAlchemyAutoSchema):
    class Meta:
        load_instance = True
        include_fk = True
