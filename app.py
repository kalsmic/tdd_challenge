from flask import (Flask, request, redirect, url_for, flash, jsonify)
from flask_migrate import Migrate
from model import db


def create_app(config='config.DevelopmentConfig'):
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

    return app
