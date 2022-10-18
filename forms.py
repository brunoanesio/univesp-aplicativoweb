from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, ValidationError, TextAreaField
from wtforms.validators import (
    Email,
    EqualTo,
    InputRequired,
    Length,
    Optional,
    Regexp,
    DataRequired,
)

from models import User


class login_form(FlaskForm):
    email = StringField(validators=[InputRequired(), Email(), Length(1, 64)])
    pwd = PasswordField(validators=[InputRequired(), Length(min=8, max=72)])
    username = StringField(validators=[Optional()])


class register_form(FlaskForm):
    username = StringField(
        validators=[
            InputRequired(),
            Length(3, 20, message="Insira um nome válido"),
            Regexp(
                "^[a-zA-Z0-9 ]*$",
                0,
                "Nome pode ter somente letras," "números, pontos ou sublinhado",
            ),
        ]
    )
    email = StringField(validators=[InputRequired(), Email(), Length(1, 64)])
    pwd = PasswordField(validators=[InputRequired(), Length(8, 72)])
    phone = StringField(validators=[DataRequired()])
    content = TextAreaField(validators=[DataRequired(), Length(-1, 200)])
    cpwd = PasswordField(
        validators=[
            InputRequired(),
            Length(8, 72),
            EqualTo("pwd", message="As senhas devem sem iguais!"),
        ]
    )

    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError("Email já foi registrado!")

    def validate_uname(self, username):
        if User.query.filter_by(username=username.data).first():
            raise ValidationError("Nome já registrado!")
