import os
import secrets
import sqlite3

# import psycopg2
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
# TODO: arrumar flask-rbac
# from flask_rbac import RBAC
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect

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
# TODO: arrumar token csrf
# csrf = CSRFProtect()
secret_key = secrets.token_hex(16)


def create_app():
    app = Flask("__name__")

    # app configs
    app.config["SECRET_KEY"] = secret_key
    app.config["SQLALCHEMY_DATABASE_URI"] = database_file
    app.config["SESSION_COOKIE_NAME"] = "my_session"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
    # jinja config
    app.jinja_env.autoescape = True

    # init flask extensions
    login_manager.init_app(app)
    db.init_app(app)
    # TODO: arrumar flask-rbac
    # rbac.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    # TODO: arrumar token csrf
    # csrf.init_app(app)

    return app
