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
        db.String(200)
    )

    def get_full_name(self):
        """ Get the first name and last name of user """

        return f"{self.first_name} {self.last_name}"

