import click
from flask import Flask
from flask.cli import with_appcontext
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy


from flaskexpense.config import Config


db = SQLAlchemy()
bcrypt = Bcrypt()
loagin_manager = LoginManager()
loagin_manager.login_view = "users.login"


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    loagin_manager.init_app(app)

    from flaskexpense.main.routes import main
    from flaskexpense.auth.routes import users
    from flaskexpense.expenses.routes import expenses
    from flaskexpense.plots.routes import plots
    from flaskexpense.errors.handlers import errors

    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(expenses)
    app.register_blueprint(plots)
    app.register_blueprint(errors)

    @click.command("create_tables")
    @with_appcontext
    def create_tables():
        db.create_all()

    app.cli.add_command(create_tables)

    return app
