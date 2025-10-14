from flask import Flask
from extensions import db, ma
from config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    ma.init_app(app)

    @app.route('/')
    def home():
        return "Welcome to the Trendmart API"


if __name__ == '__main__':
    app = create_app()

    with app.app_context():
        db.create_all()
        print("Database tables created!")

    app.run(debug=True)
