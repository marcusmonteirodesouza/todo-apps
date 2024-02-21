import logging
import sys
import flask_migrate
from flask import Flask

from .config import config
from .db import db, migrate
from .error_handlers import add_error_handlers
from .todos.services import TodosService
from .todos.blueprints import todos_blueprint


def create_app():
    logging.basicConfig(stream=sys.stdout, level=config.LOG_LEVEL)

    app = Flask(__name__)

    app.config.from_object(config)

    db.init_app(app=app)
    migrate.init_app(app=app, db=db)

    app.todos_service = TodosService()

    app.register_blueprint(blueprint=todos_blueprint)

    add_error_handlers(app=app)

    return app


def setup_database(app: Flask):
    with app.app_context():
        db.create_all()
        flask_migrate.upgrade()


def setup_app():
    app = create_app()
    setup_database(app=app)

    return app
