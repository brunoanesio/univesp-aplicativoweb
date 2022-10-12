import os
import secrets
import sqlite3

from authlib.integrations.flask_client import OAuth

# import psycopg2
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# SQLite DB
project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "database.db"))


def get_db_connection():
    conn = sqlite3.connect("database.db")
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
ma = Marshmallow()
migrate = Migrate()
bcrypt = Bcrypt()
oauth = OAuth()
secret_key = secrets.token_hex(16)


def create_app():
    app = Flask("__name__")

    # app configs
    app.config["SECRET_KEY"] = secret_key
    app.config["SQLALCHEMY_DATABASE_URI"] = database_file
    app.config["SESSION_COOKIE_NAME"] = "my_session"
    app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
    app.config["GOOGLE_CLIENT_ID"] = os.getenv("GOOGLE_CLIENT_ID")
    app.config["GOOGLE_CLIENT_SECRET"] = os.getenv("GOOGLE_CLIENT_SECRET")
    # jinja config
    app.jinja_env.autoescape = True

    # init flask extensions
    login_manager.init_app(app)
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    oauth.init_app(app)

    return app
