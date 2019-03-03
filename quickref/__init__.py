from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from .config import Config


def create_app(test=False):
    """
    App factory.

    :param test: If True, creates a testing instance.

    :returns: A Flask App instance.
    """
    app = Flask(__name__)
    app.config.from_object(Config)

    Bootstrap(app)

    return app


app = create_app()

# Set up database
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# User login
login = LoginManager(app)
login.login_view = 'login'

from . import routes
from .models import user