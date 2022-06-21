"""
This module contains the application setup
"""
from flask import (Flask)
from flask_migrate import Migrate

from api.users import users_bp
from model import db


def create_app(config='config.DevelopmentConfig'):
    """
    Create and configure an instance of the Flask application."""
    app = Flask(__name__)

    app.config.from_object(config)

    # Initialize the database
    db.init_app(app)

    # Initialize the migration engine
    migrate = Migrate()
    migrate.init_app(app, db)

    @app.route('/')
    def index():
        return 'Hello, TDD!'

    app.register_blueprint(users_bp)

    return app
