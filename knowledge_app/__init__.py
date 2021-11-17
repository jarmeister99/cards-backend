from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

import os


def create_app() -> Flask:
    """
    Factory function to return a WSGI-compliant Flask instance
    :return: A Flask instance
    """
    app = Flask(__name__)

    # load middleware
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # load dotenv in base root
    APP_ROOT = os.path.dirname(__file__)  # refers to application_top
    dotenv_path = os.path.join(APP_ROOT, ".flaskenv")
    load_dotenv(dotenv_path)

    # import routes to register them
    with app.app_context():
        import knowledge_app.api.routes
        from knowledge_app.db.db import client
    return app
