"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
dbx = db.session.execute

class User(db.Model):

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
        db.String(1000),
    ) # TODO: add default and null=false

    post = db.relationship(
        "Post",
        back_populates="User",
        cascade="all, delete-orphan"
        )


    def get_full_name(self):
        """ Get the first name and last name of user """

        return f"{self.first_name} {self.last_name}" # TODO: make into property




class Post(db.Model):

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
        db.DateTime(timezone=True),
        nullable=False,
    ) # TODO: Does this work as expected?

    id = db.mapped_column(
        db.Integer,
        db.ForeignKey(
            "users.id",
            ondelete="CASCADE",
            onupdate="CASCADE",
            nullable=False
        )
    )

    user = db.relationship(
        "User",
        back_populates="post"
    )