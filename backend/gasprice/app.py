import os

from flask import Flask
from flask_cors import CORS


def create_app(config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('gasprice.config')
    if app.config['ENV'] == 'production':
        app.config.from_object('gasprice.prod_config')

    # Override config if any (test env)
    if config:
        app.config.from_mapping(config)

    CORS(app, resources={r"/*": {"origins": app.config['CORS_WHITELIST']}})

    # Register routes
    from . import (
        services
    )

    services.init_app(app)

    return app
