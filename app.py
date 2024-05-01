"""Blogly application."""

import os

from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension

from models import db, dbx, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///blogly')

app.config['SQLALCHEMY_ECHO'] = True
db.init_app(app)

app.config['SECRET_KEY'] = os.environ.get(
    'SECRET_KEY', "ANYA AND ALICE's SECRET!")
print("secret key =", app.config['SECRET_KEY'])
debug = DebugToolbarExtension(app)


@app.get("/")
def homepage():
    """Return movie list."""

    q_movies = db.select(Movie)
    movies = dbx(q_movies).scalars().all()

    q_studios = db.select(Studio)
    studios = dbx(q_studios).scalars().all()
    return render_template("movies_list.jinja", movies=movies, studios=studios)
