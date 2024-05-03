"""Models for Blogly."""

import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
dbx = db.session.execute

DEFAULT_IMAGE_URL = "https://via.placeholder.com/250"

class User(db.Model):
    """ User class """

    __tablename__ = "users"

    id = db.mapped_column(
        db.Integer,
        db.Identity(),
        primary_key=True,
    )

    first_name = db.mapped_column(
        db.String(50),
        nullable=False,
    )

    last_name = db.mapped_column(
        db.String(50),
        nullable=False,
    )

    image_url = db.mapped_column(
        db.String(2048),
        default=DEFAULT_IMAGE_URL,
        nullable=False
    )

    posts = db.relationship(
        "Post",
        back_populates="user",
        cascade="all, delete-orphan"
        )


    def get_full_name(self):
        """ Get the first name and last name of user """

        return f"{self.first_name} {self.last_name}" # TODO: make into property




class Post(db.Model):
    """ Blog post """

    __tablename__ = "posts"

    id = db.mapped_column(
        db.Integer,
        db.Identity(),
        primary_key=True,
    )

    title = db.mapped_column(
        db.String(1000),
        nullable=False,
    )

    content = db.mapped_column(
        db.Text,
        nullable=False,
    )

    created_at = db.mapped_column(
        db.DateTime,
        default=datetime.datetime.now,
        nullable=False,
    ) # TODO: Does this work as expected?

    user_id = db.mapped_column(
        db.Integer,
        db.ForeignKey("users.id",ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False
    )

    user = db.relationship(
        "User",
        back_populates="posts"
    )

    @property
    def friendly_date(self):
        """Return nicely-formatted date."""

        return self.created_at.strftime("%a %b %-d  %Y, %-I:%M %p")
