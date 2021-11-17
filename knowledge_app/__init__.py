from flask import Flask


def create_app() -> Flask:
    """
    Factory function to return a WSGI-compliant Flask instance
    :return: A Flask instance
    """
    app = Flask(__name__)

    # import routes to register them
    with app.app_context():
        import knowledge_app.api.routes
    return app
