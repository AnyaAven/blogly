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
    """Returns to list of users"""

    q_user = db.select(User)
    users = dbx(q_user).scalars().all()
    # ['Alice Chang','A.A', ...]
    user_full_names = [u.get_full_name() for u in users]

    user_ids = [u.id for u in users]
    # [1, 2]

    return render_template(
        "user_listing.jinja",
        user_ids=user_ids,
        user_full_names=user_full_names)
