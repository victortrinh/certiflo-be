import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

from .config import config_by_name
from .middleware.error_handlers import register_error_handlers
from .middleware.rate_limiter import limiter

db = SQLAlchemy()
flask_bcrypt = Bcrypt()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    if config_name == 'prod':
        if not os.environ.get('SECRET_KEY'):
            raise ValueError('SECRET_KEY environment variable is required in production')
        if not app.config.get('SQLALCHEMY_DATABASE_URI'):
            raise ValueError('DATABASE_URL environment variable is required in production')

    db.init_app(app)
    flask_bcrypt.init_app(app)
    limiter.init_app(app)

    register_error_handlers(app)

    @app.after_request
    def set_security_headers(response):
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-XSS-Protection'] = '0'
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        response.headers['Permissions-Policy'] = 'geolocation=(), camera=(), microphone=()'
        if not app.debug:
            response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        return response

    return app
