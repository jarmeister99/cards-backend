from flask import Flask


def create_app() -> Flask:
    """
    Factory function to return a WSGI-compliant Flask instance
    :return: A Flask instance
    """
    app = Flask(__name__)
    return app
