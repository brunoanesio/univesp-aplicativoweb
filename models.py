import datetime

from flask_security.core import RoleMixin, UserMixin

from app import db, ma

roles_users = db.Table(
    "roles_users",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
    db.Column("role_id", db.Integer, db.ForeignKey("role.id")),
)


class Role(db.Model, RoleMixin):
    __tablename__ = "role"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))

    def __str__(self):
        return self.name


class User(db.Model, UserMixin):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(12), nullable=False)
    content = db.Column(db.String(200), nullable=False)
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


class UserSchema(ma.Schema):
    class Meta:
        # fields = ("username", "email")
        fields = ("username", "email", "phone", "content")


user_schema = UserSchema()
users_schema = UserSchema(many=True)
