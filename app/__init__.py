from flask import Flask
from flask_migrate import Migrate
from .models import *
from .utils import *
from .views import view_blueprint
from .cli import cli_blueprint


def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI='sqlite:///project.db'
    )
    db.init_app(app)
    migrate = Migrate(app, db)
    with app.app_context():
        db.create_all()
    app.register_blueprint(view_blueprint)
    app.register_blueprint(cli_blueprint)
    return app

app = create_app()
