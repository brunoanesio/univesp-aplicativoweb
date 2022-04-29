import datetime

from flask_login import UserMixin

from app import db


class User(UserMixin, db.Model):  # type: ignore
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    pwd = db.Column(db.String(300), nullable=False, unique=True)

    def __repr__(self):
        return '<User %r' % self.username


class Posts(db.Model):  # type: ignore
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    title = db.Column(db.String(80), nullable=False)
    telefone = db.Column(db.String(11), nullable=False)
    content = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return '<title %r' % self.id
