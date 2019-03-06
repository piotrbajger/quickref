from flask import Flask

from .config import Config, TestConfig
from .routes.static import static
from .routes.refs import refs
from .extensions import bootstrap, db, migrate, login_manager


def create_app(test=False):
    """
    App factory.

    :param test: If True, creates a testing instance.

    :returns: A Flask App instance.
    """
    app = Flask(__name__)

    if test:
        app.config.from_object(TestConfig)
    else:
        app.config.from_object(Config)

    register_blueprints(app)
    register_extensions(app)

    return app


def register_blueprints(app):
    print("Registering blueprints.")
    app.register_blueprint(static, template_folder='templates')
    app.register_blueprint(refs, template_folder='templates')


def register_extensions(app):
    print("Registering extensions.")
    bootstrap.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)