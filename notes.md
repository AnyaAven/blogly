# Blogly

- make sure we setup everything
- venv
```shell
```shell
my_dir $ python3 -m venv venv

my_dir $ source venv/bin/activate

(venv) my_dir $ pip3 install flask setuptools

(venv) my_dir $ pip3 install ipython

(venv) $ pip3 install psycopg2-binary flask-sqlalchemy
(venv) $ pip3 install flask-debugtoolbar setuptools

(venv) my_dir $ pip3 freeze > requirements.txt

(venv) my_dir $ git status

(venv) my_dir $ echo "node_modules\n.vite\nvenv/\n__pychache__" > .gitignore

```

- sql alchemy code within python (idk what file)

```python
import os
from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from werkzeug.exceptions import NotFound

from models import db, dbx, Movie, Studio #swap out these classes depending on project

app = Flask(__name__)

# note: it is URI, not URL
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///sqla_movies') #swap this out depending on DB being used

app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_RECORD_QUERIES'] = True
db.init_app(app)

```

- flask secretkey -- TO ADD
- environmental variable??
- templates jinja - (madlibs)


1. Create User Model class within models.py
    - ***To create the table, need fields:***
        - User ID (auto-generated, primary key)
        - first_name
        - last_name
        - image_url
            - Decide which fields should be required

```python
class Studio(db.Model):
    """Movie studio."""

    __tablename__ = "studios"

    code = db.mapped_column(
        db.String(10),
        primary_key=True,
    )

    name = db.mapped_column(
        db.String(50),
        unique=True,
        nullable=False,
    )

    founded = db.mapped_column(
        db.Date,
    )
```
2. Create a method within user model class
- ***Create a method to  get_full_name ***

```python
        class Movie(db.Model):  # ...
            def is_kid_safe(self):
        """Is this film safe for kids?"""

                return self.rating in ('G', 'PG')
```


3. Create Flask App (app.py)
- Create the DB
```shell
createdb sqla_movies #change name
```
- Import the user model
- Create the tables for user model
    - demo/seed.py (insert data )




## Concerns
- Who is handling the caps of first or last name? UI, models.py, or app.py?
