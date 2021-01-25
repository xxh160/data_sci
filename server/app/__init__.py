from flask import Flask

from app.analyzer import analysis


def create_app(config_object):
    app = Flask(__name__)
    app.config.from_object(config_object)
    app.register_blueprint(analysis, url_prefix="/api/v1/analyzer")
    return app
