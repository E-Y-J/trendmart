from flask import Flask, send_from_directory
from extensions import db, ma, jwt, init_stripe
from config import Config
from routes.catalog import categories_bp, products_bp
from routes.auth import auth_bp
from routes.customers import customers_bp
import models
from flask_swagger_ui import get_swaggerui_blueprint
import os

SWAGGER_URL = '/api/docs' 
API_URL = '/api/swagger'  # URL to serve our swagger file

# Create swaggerui blueprint
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Trendmart API Documentation",
    }
)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)

    init_stripe(app)

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(customers_bp)
    app.register_blueprint(categories_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(swaggerui_blueprint)

    # Route to serve swagger.yaml file
    @app.route('/api/swagger')
    def swagger_spec():
        return send_from_directory('documentation', 'swagger.yaml')

    @app.route('/')
    def home():
        return "Welcome to the Trendmart API"

    return app


if __name__ == '__main__':
    app = create_app()

    with app.app_context():
        # db.drop_all()
        db.create_all()
        print("Database tables created!")

    app.run(debug=True)
