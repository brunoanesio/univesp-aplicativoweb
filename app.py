import os
# import psycopg2
import sqlite3

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
# TODO: arrumar flask-rbac
# from flask_rbac import RBAC
from flask_sqlalchemy import SQLAlchemy

# SQLite DB
project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "database.db"))


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn
# PostgreSQL
# uri = os.getenv("DATABASE_URL")
# if uri.startswith("postgres://"):
#     uri = uri.replace("postgres://", "postgresql://", 1)
# conn = psycopg2.connect(uri, sslmode="require")


# Login
login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "login"  # type: ignore
login_manager.login_message_category = "info"

db = SQLAlchemy()
# TODO: arrumar flask-rbac
# rbac = RBAC()
migrate = Migrate()
bcrypt = Bcrypt()


def create_app():
    app = Flask("__name__")

    app.config["SECRET_KEY"] = "your secret key"
    app.config["SQLALCHEMY_DATABASE_URI"] = database_file
    app.config["SESSION_COOKIE_NAME"] = "my_session"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

    login_manager.init_app(app)
    db.init_app(app)
    # TODO: arrumar flask-rbac
    # rbac.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)

    return app
