from flask import Flask

from app.routes import main, swagger


def create_app():
    app = Flask(__name__)
    app.register_blueprint(main)
    app.register_blueprint(swagger, url_prefix="/")
    return app
