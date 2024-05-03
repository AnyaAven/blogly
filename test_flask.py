import os

os.environ["DATABASE_URL"] = "postgresql:///blogly_test"
os.environ["FLASK_DEBUG"] = "0"

from unittest import TestCase

from app import app
from models import db, dbx, User

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

app.app_context().push()
db.drop_all()
db.create_all()


class UserViewTestCase(TestCase):
    """Test views for users."""

    def setUp(self):
        """Create test client, add sample data."""

        db.session.rollback()

        # As you add more models later in the exercise, you'll want to delete
        # all of their records before each test just as we're doing with the
        # User model below.
        dbx(db.delete(User))
        db.session.commit()

        test_user = User(
            first_name="test1_first",
            last_name="test1_last",
            image_url=None
        )

        db.session.add(test_user)
        db.session.commit()

        # We can hold onto our test_user's id by attaching it to self (which is
        # accessible throughout this test class). This way, we'll be able to
        # rely on this user in our tests without needing to know the numeric
        # value of their id, since it will change each time our tests are run.
        self.user_id = test_user.id

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_list_users(self):
        with app.test_client() as c:
            resp = c.get("/users")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("test1_first", html)
            self.assertIn("test1_last", html)
            self.assertIn("<!-- Test comment for user_listing -->", html)

    def test_adding_user(self):
        with app.test_client() as c:
            d = {
                "first_name": "Test2_first",
                "last_name": "Test2_last",
                "image_url": "", # FIXME: what about default image?
            }

            resp = c.post("/users/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Test2_first", html)
            self.assertIn("Test2_last", html)
            self.assertIn("<!-- Test comment for user_listing -->", html)

    def test_editing_users_form(self):
        with app.test_client() as c:
            resp = c.get(f"/users/{self.user_id}/edit")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("<!-- Test comment for edit_user_form -->", html)

    def test_editing_user(self):
        with app.test_client() as c:
            d = {
                "first_name": "Test_first_EDITED",
                "last_name": "Test_last_EDITED",
                "image_url": "",
            }

            resp = c.post(
                f"/users/{self.user_id}/edit",
                data=d,
                follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Test_first_EDITED", html)
            self.assertIn("Test_last_EDITED", html)
            self.assertIn("<!-- Test comment for user_listing -->", html)

    def test_deleting_user(self):
        with app.test_client() as c:
            #ensure id doesn't exist in database/main page
            resp = c.post(
                f"/users/{self.user_id}/delete",
                follow_redirects=True)
            html = resp.get_data(as_text=True)

            # FIXME: Should test the the database WHILE testing the HTML
            # db.select() works
            # Everything that works in SQLA can be done here!
            # It is a good idea to test the full journey
            # We don't want to seperate the DB and the UI
            # We want to test both at once.
            # Eventually the classes will be seperated more
            # EX: DeleteUserViewTest
            # EX: EditUserViewTest
            # View Function, saying view test refers to testing the route

            # FIXME: Add the negative test
            # What if the firstname submitted was 2000 chars long?
            # What if someone tries to go to a user that doesn't exist? 404!

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn("test1_first", html)
            self.assertNotIn("test1_last", html)
            self.assertIn("<!-- Test comment for user_listing -->", html)



