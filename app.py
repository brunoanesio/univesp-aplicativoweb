import datetime
import os
import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from werkzeug.exceptions import abort

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "database.db"))


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


app = Flask('__name__')
app.config['SECRET_KEY'] = 'your secret key'
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
db = SQLAlchemy(app)


class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    title = db.Column(db.String(80), nullable=False)
    content = db.Column(db.String(200), nullable=False)


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

        if not title:
            flash('O título é obrigatório!')
        else:
            post = Posts(title=title, content=content)
            db.session.add(post)
            db.session.commit()
            return redirect(url_for('index'))

    return render_template('create.html')


# Erro na hora de editar o post
# @app.route('/<int:id>/edit', methods=('GET', 'POST'))
# def edit(id):
#    post = get_post(id)
#    
#    if request.method == 'POST':
#        title = request.form['title']
#        content = request.form['create']
#
#        if not title:
#            flash('O título é obrigatório!')
#        else:
#            post.title = title
#            post.content = content
#            db.session.commit()
#            return redirect(url_for('index'))
#
#    return render_template('edit.html', post=post)

if __name__ == "__main__":
    app.run(debug=True)
