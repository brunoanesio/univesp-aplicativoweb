import datetime

from flask_security.core import RoleMixin, UserMixin

from app import db

roles_users = db.Table(
    "roles_users",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
    db.Column("role_id", db.Integer, db.ForeignKey("role.id")),
)


class Role(db.Model, RoleMixin):  # type: ignore
    __tablename__ = "role"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))

    def __str__(self):
        return self.name


class User(db.Model, UserMixin):  # type: ignore
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    pwd = db.Column(db.String(300), nullable=False, unique=True)
    fs_uniquifier = db.Column(db.String(64), unique=True, nullable=False)
    roles = db.relationship(
        "Role", secondary=roles_users, backref=db.backref("users", lazy="joined")
    )

    def active(self):
        return True

    def is_active(self):
        return True

    def __repr__(self):
        return "<User %r" % self.email


class Posts(db.Model):  # type: ignore
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    title = db.Column(db.String(80), nullable=False)
    telefone = db.Column(db.String(11), nullable=False)
    content = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return "<title %r" % self.id
