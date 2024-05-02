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
def redirect_to_users():
    """ Redirect to users

    WIP, add more to this later
    """

    return redirect("/users")

@app.get("/users")
def display_users_list():
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


@app.get("/users/new")
def display_new_user_form():
    """ Display new user form """

    return render_template("new_user_form.jinja")

@app.post("/users/new")
def add_user():
    """ Add new user to the database and redirect to /users """

    fname = request.form['first_name']
    lname = request.form['last_name']

    # Use user's image url or the default img url
    img_url = request.form.get("image_url", "https://via.placeholder.com/250") # FIXME: global URL


    new_user = User(first_name=fname, last_name=lname, image_url=img_url)

    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")

