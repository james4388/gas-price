"""Init all api route with main app
"""


def init_app(app):
    from .gasfeed import gasfeed_bp
    from .geocoding import geocoding_bp
    from .clearbit import clearbit_bp

    app.register_blueprint(gasfeed_bp, url_prefix='/gasfeed')
    app.register_blueprint(geocoding_bp, url_prefix='/geocoding')
    app.register_blueprint(clearbit_bp, url_prefix='/clearbit')
