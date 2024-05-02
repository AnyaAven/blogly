"""Blogly application."""

import os

from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension

from models import db, dbx, User

DEFAULT_URL = "https://via.placeholder.com/250" # TODO: Move to user model

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
    # [<User 1>, <User 2> ...]

    user_mapping = {}

    # access list of users, pull out id and name for each user instance
    for user in users:
        user_mapping[user.id] = user.get_full_name()

    return render_template(
        "user_listing.jinja",
        user_mapping=user_mapping)


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
    img_url = request.form["image_url"] or DEFAULT_URL

    new_user = User(first_name=fname, last_name=lname, image_url=img_url)

    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")

@app.get("/users/<int:user_id>")
def show_user(user_id):
    """Shows information about the given user"""

    #search for the user instance by id
    q_user = db.select(User).where(User.id == user_id)
    user_detail = dbx(q_user).scalars().one()
    # send the info to user_detail page
    user_full_name = user_detail.get_full_name()
    user_image = user_detail.image_url
    user_id = user_detail.id

    return render_template(
        "user_detail.jinja",
        user_full_name=user_full_name,
        user_image=user_image,
        user_id=user_id
        )

@app.post("/users/<int:user_id>/delete")
def delete_user(user_id):
    """ Doc """