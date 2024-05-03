"""Blogly application."""

import os

from flask import Flask, request, redirect, render_template, flash
from flask_debugtoolbar import DebugToolbarExtension

from models import db, dbx, User, Post

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

    q_user = db.select(User).order_by(User.first_name)
    users = dbx(q_user).scalars().all()
    # [<User 1>, <User 2> ...]

    return render_template(
        "user_listing.jinja",
        users=users)


@app.get("/users/new")
def display_new_user_form():
    """ Display new user form """

    return render_template("new_user_form.jinja")


@app.post("/users/new")
def add_user():
    """ Add new user to the database and redirect to /users
    If user does not provide a image url, add a default url image
    """

    fname = request.form['first_name']
    lname = request.form['last_name']

    # Use user's image url or the default img url
    img_url = request.form["image_url"] or None # FIXME: does this work as intended?

    new_user = User(first_name=fname, last_name=lname, image_url=img_url)

    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")


@app.get("/users/<int:user_id>")
def show_user(user_id):
    """ Show information about the user and their posts """

    # Note: WHAT IF we don't have a user id of 99? use 404!
    user = db.get_or_404(User, user_id)

    posts = user.posts

    # Note: You can pass in the user instance to jinja instead and use the attributes
    return render_template(
        "user_detail.jinja",
        user=user,
        posts=posts
    )

@app.get("/users/<int:user_id>/edit")
def show_edit_user_form(user_id):
    """Show the edit page for a user."""

    user = db.get_or_404(User, user_id)

    return render_template(
        "edit_user_form.jinja",
        user=user
    )


@app.post("/users/<int:user_id>/edit")
def edit_user(user_id):
    """Get values from user inputs from edit user form and changing the DB."""

    user = db.get_or_404(User, user_id)

    # This is similar to a patch request
    # This doesn't allow us to ever remove our image, populate it at this function instead
    # "/users/<int:user_id>/edit")
    # def show_edit_user_form(user_id):
    # Then remove the or on lines 134, 134, and 136

    # if value is blank, leave as is
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    img_url = request.form["image_url"]

    # update the DB with updated user info
    user.first_name = first_name
    user.last_name = last_name
    user.image_url = img_url
    db.session.commit()

    return redirect("/users")


@app.post("/users/<int:user_id>/delete")
def delete_user(user_id):
    """ Delete user from database and redirect to /users """

    # Question: 404 here? Browser shows "post method not allowed "
    # No need to fix that, that only happens if the user is a bad actor

    # You can make post requests from more places than just a browser
    # (Think insomnia or the shell!) so using get_or_404 is still good from other places.
    user = db.get_or_404(User, user_id)
    db.session.delete(user)

    db.session.commit()

    return redirect("/users")


""" *********************** POSTS ****************************************** """

@app.get("/users/<int:user_id>/posts/new")
def show_new_post_form(user_id):
    """Show the new post form for a user."""

    return render_template("new_post_form.jinja", user_id=user_id)


@app.post("/users/<int:user_id>/posts/new")
def add_new_post(user_id):
    """ Adds new post to the DB and displays it under the user detail page """
    title = request.form['title']
    content = request.form['content']

    errs = []
    if not title:
        errs.append("You need a title to post")
    if not content:
        errs.append("You need content for your post")

    if errs:
        for err in errs:
            flash(err)

        route =  f"/users/{user_id}/posts/new"
        return render_template(
            "new_post_form.jinja",
            user_id=user_id,
            current_page=route
        )


    new_post = Post(title=title, content=content, user_id=user_id)

    db.session.add(new_post)
    db.session.commit()

    return redirect(f"/users/{user_id}")

@app.get("/posts/<int:post_id>")
def display_post(post_id):
    """ Display the post """
    # TODO: Does this work? Need to pass the user inst and post inst

    post = db.get_or_404(Post, post_id)

    user = post.user

    return render_template(
        "post_detail.jinja",
        user=user,
        post=post
    )