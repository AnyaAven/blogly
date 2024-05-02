import os
from unittest import TestCase

os.environ["DATABASE_URL"] = "postgresql:///blogly_test"
os.environ["FLASK_DEBUG"] = "0"

from app import app
from models import db, dbx, User

app.app_context().push()

db.drop_all()
db.create_all()


class UserModelTestCase(TestCase):
    def setUp(self):
        dbx(db.delete(User))
        db.session.commit()

    def tearDown(self):
        db.session.rollback()

    def test_get_full_name(self): #TODO: change the name of this if we have a @property
        test_user = User(first_name="Test", last_name="Rabbit")
        self.assertEqual(test_user.get_full_name(), "Test Rabbit")

    def test_add_user(self):
        test_user = User(first_name="Test", last_name="Rabbit")
        db.session.add(test_user)
        db.session.commit()
        self.assertIsInstance(test_user.id, int)

