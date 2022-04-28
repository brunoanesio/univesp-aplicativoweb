from flask import (
    Flask,
    render_template,
    redirect,
    request,
    flash,
    url_for,
    session
)

from datetime import timedelta
from sqlalchemy.exc import (
    IntegrityError,
    DataError,
    DatabaseError,
    InterfaceError,
    InvalidRequestError,
)
from werkzeug.routing import BuildError
from werkzeug.exceptions import abort


from flask_bcrypt import Bcrypt, generate_password_hash, check_password_hash

from flask_login import (
    UserMixin,
    login_user,
    LoginManager,
    current_user,
    logout_user,
    login_required,
)

from app import create_app, db, login_manager, bcrypt
from models import User, Posts
from forms import login_form, register_form


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


app = create_app()


@app.before_request
def session_handler():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=1)


@app.route('/', methods=("GET", "POST"), strict_slashes=False)
def index():
    posts = Posts.query.all()
    return render_template('index.html', posts=posts)


def get_post(post_id):
    post = Posts.query.filter_by(id=post_id).first()
    if post is None:
        abort(404)
    return post


@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)


@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['create']
        telefone = request.form['telefone']

        if not title or not content or not telefone:
            flash('É obrigatório preencher todas as informações!')
        else:
            post = Posts(title=title, content=content, telefone=telefone)
            db.session.add(post)
            db.session.commit()
            return redirect(url_for('index'))

    return render_template('create.html')


@app.route('/edit/<int:id>', methods=('GET', 'POST'))
def edit(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['create']
        telefone = request.form['telefone']

        if not title or not content:
            flash('É obrigatório preencher todas as informações!')
        else:
            post.title = title
            post.content = content
            post.telefone = telefone
            db.session.commit()
            return redirect(url_for('index'))

    return render_template('edit.html', post=post)


@app.route('/delete/<int:id>', methods=('GET', 'POST'))
def delete(id):
    post = get_post(id)

    try:
        db.session.delete(post)
        db.session.commit()
        return redirect(url_for('index'))
    except:
        return "Erro na hora de deletar o post."


@app.route("/login/", methods=("GET", "POST"), strict_slashes=False)
def login():
    form = login_form()

    if form.validate_on_submit():
        try:
            user = User.query.filter_by(email=form.email.data).first()
            if check_password_hash(user.pwd, form.pwd.data):
                login_user(user)
                return redirect(url_for('index'))
            else:
                flash("Nome ou senha invalidos!", "danger")
        except Exception as e:
            flash(e, "danger")

    return render_template("auth.html",
                           form=form,
                           text="Login",
                           title="Login",
                           btn_action="Login"
                           )


@app.route("/register/", methods=("GET", "POST"), strict_slashes=False)
def register():
    form = register_form()
    if form.validate_on_submit():
        try:
            email = form.email.data
            pwd = form.pwd.data
            username = form.username.data

            newuser = User(
                username=username,
                email=email,
                pwd=bcrypt.generate_password_hash(pwd).decode('utf-8'),
            )

            db.session.add(newuser)
            db.session.commit()
            flash(f"Conta criada com sucesso", "success")
            return redirect(url_for("login"))

        except InvalidRequestError:
            db.session.rollback()
            flash(f"Algo deu errado!", "danger")
        except IntegrityError:
            db.session.rollback()
            flash(f"Usuário já existe!", "warning")
        except DataError:
            db.session.rollback()
            flash(f"Entrada invalida", "warning")
        except InterfaceError:
            db.session.rollback()
            flash(f"Erro ao conectar ao banco de dados", "danger")
        except DatabaseError:
            db.session.rollback()
            flash(f"Erro ao conectar ao banco de dados", "danger")
        except BuildError:
            db.session.rollback()
            flash(f"Um erro ocorreu!", "danger")

    return render_template("auth.html",
                           form=form,
                           text="Crie uma conta",
                           title="Criação de conta",
                           btn_action="Criar conta"
                           )


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug=True)
