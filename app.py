import datetime
import os
import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from werkzeug.exceptions import abort

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "postgres://zqengaugwztmer:2957421213882db43c2d51b7be8993a1cd2dad43cec97fc2cf9fe80601ffdaf9@ec2-54-157-16-125.compute-1.amazonaws.com:5432/d954gkdth7qsmv".format(os.path.join(project_dir, "database.db"))


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


app = Flask('__name__')
app.config['SECRET_KEY'] = 'your secret key'
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config['SESSION_COOKIE_NAME'] = "my_session"
db = SQLAlchemy(app)


class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    title = db.Column(db.String(80), nullable=False)
    telefone = db.Column(db.Integer)
    content = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return '<title %r' % self.id


@app.route('/')
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


if __name__ == "__main__":
    app.run(debug=False)
