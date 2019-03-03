from flask import Flask
from flask_bootstrap import Bootstrap
from .config import Config


def create_app(test=False):
    """
    App factory.

    :param test: If True, creates a testing instance.

    :returns: A Flask App instance.
    """
    app = Flask(__name__)
    app.config.from_object(Config)

    return app


app = create_app()
Bootstrap(app)


from . import routes