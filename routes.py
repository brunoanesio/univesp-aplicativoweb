from datetime import timedelta

from flask import flash, redirect, render_template, request, session, url_for
from flask_bcrypt import check_password_hash
from flask_login import login_user, logout_user
from flask_security import (Security, SQLAlchemyUserDatastore, login_required,
                            roles_accepted)
from sqlalchemy.exc import (DatabaseError, DataError, IntegrityError,
                            InterfaceError, InvalidRequestError)
from werkzeug.exceptions import abort
from werkzeug.routing import BuildError

from app import (bcrypt, create_app, db,  # TODO: arrumar flask-rbac
                 login_manager)
from forms import login_form, register_form
from models import Posts, Role, User


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# TODO: arrumar flask-rab
# @rbac.set_user_loader
# def get_current_user():
#     return current_user._get_current_object()


app = create_app()
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)


@app.before_first_request
def create_roles():
    user_datastore.create_role(name='admin')
    user_datastore.create_role(name='guest')


@app.before_request
def session_handler():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=60)


@app.route("/", methods=("GET", "POST"), strict_slashes=False)
def index():
    posts = Posts.query.all()
    return render_template("index.html", posts=posts)


@app.route("/dashboard", methods=("GET", "POST"))
@login_required
@roles_accepted('admin')
def dashboard():
    posts = Posts.query.all()
    return render_template("admin.html", posts=posts)


def get_post(post_id):
    post = Posts.query.filter_by(id=post_id).first()
    if post is None:
        abort(404)
    return post


@app.route("/<int:post_id>")
def post(post_id):
    post = get_post(post_id)
    return render_template("post.html", post=post)


@app.route("/create", methods=("GET", "POST"))
@login_required
def create():
    if request.method == "POST":  # type: ignore
        title = request.form["title"]  # type: ignore
        content = request.form["create"]  # type: ignore
        telefone = request.form["telefone"]  # type: ignore

        if not title or not content or not telefone:
            flash("É obrigatório preencher todas as informações!", "info")
        else:
            post = Posts(title=title, content=content, telefone=telefone)
            db.session.add(post)
            db.session.commit()
            return redirect(url_for("index"))

    return render_template("create.html")


@app.route("/edit/<int:id>", methods=("GET", "POST"))
@login_required
def edit(id):
    post = get_post(id)

    if request.method == "POST":  # type: ignore
        title = request.form["title"]  # type: ignore
        content = request.form["create"]  # type: ignore
        telefone = request.form["telefone"]  # type: ignore

        if not title or not content:
            flash("É obrigatório preencher todas as informações!", "info")
        else:
            post.title = title
            post.content = content
            post.telefone = telefone
            db.session.commit()
            return redirect(url_for("index"))

    return render_template("edit.html", post=post)


@app.route("/delete/<int:id>", methods=("GET", "POST"))
@login_required
def delete(id):
    post = get_post(id)

    try:
        db.session.delete(post)
        db.session.commit()
        return redirect(url_for("index"))
    except Exception as e:
        flash(e, "Erro na hora de deletar o post.")


@app.route("/login/", methods=("GET", "POST"), strict_slashes=False)
def login():
    form = login_form()

    if form.validate_on_submit():
        try:
            user = User.query.filter_by(email=form.email.data).first()
            if check_password_hash(user.pwd, form.pwd.data):
                login_user(user)
                return redirect(url_for("index"))
            else:
                flash("Nome ou senha invalidos!", "danger")
        except Exception as e:
            flash(e, "danger")

    return render_template(
        "login.html", form=form, text="Login", title="Login", btn_action="Login"
    )


@app.route("/register/", methods=("GET", "POST"), strict_slashes=False)
def register():
    form = register_form()
    if form.validate_on_submit():
        try:
            email = form.email.data
            pwd = form.pwd.data
            username = form.username.data

            newuser = User(  # type: ignore
                username=username,
                email=email,
                pwd=bcrypt.generate_password_hash(pwd).decode("utf-8"),
                roles=[]
            )
            default_role = user_datastore.find_or_create_role('guest')
            user_datastore.add_role_to_user(newuser, default_role)

            db.session.add(newuser)
            db.session.commit()
            flash("Conta criada com sucesso", "success")
            return redirect(url_for("login"))

        except InvalidRequestError:
            db.session.rollback()
            flash("Algo deu errado!", "danger")
        except IntegrityError:
            db.session.rollback()
            flash("Usuário já existe!", "warning")
        except DataError:
            db.session.rollback()
            flash("Entrada invalida", "warning")
        except InterfaceError:
            db.session.rollback()
            flash("Erro ao conectar ao banco de dados", "danger")
        except DatabaseError:
            db.session.rollback()
            flash("Erro ao conectar ao banco de dados", "danger")
        except BuildError:
            db.session.rollback()
            flash("Um erro ocorreu!", "danger")

    return render_template(
        "login.html",
        form=form,
        text="Crie uma conta",
        title="Criação de conta",
        btn_action="Criar conta",
    )


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

# TODO: redirecionar corretamente para pagina de login
@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
