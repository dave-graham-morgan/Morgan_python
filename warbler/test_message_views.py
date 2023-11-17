"""Message View tests."""

# run these tests like:
#
#    FLASK_ENV=production python -m unittest test_message_views.py


import os
from unittest import TestCase
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound


from models import db, connect_db, Message, User, Likes

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app

from app import app, CURR_USER_KEY

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()

# Don't have WTForms use CSRF at all, since it's a pain to test

app.config['WTF_CSRF_ENABLED'] = False


class MessageViewTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()

        self.client = app.test_client()

        self.testuser = User.signup(username="testuser",
                                    email="test@test.com",
                                    password="testuser",
                                    image_url=None)
        
        self.testuser2 = User.signup(username="testuser2",
                                    email="test2@test.com",
                                    password="testuser2",
                                    image_url=None)

        db.session.commit()

    def test_add_message(self):
        """Can user add a message?"""

        # Since we need to change the session to mimic logging in,
        # we need to use the changing-session trick:

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            # Now, that session setting is saved, so we can have
            # the rest of ours test

            resp = c.post("/messages/new", data={"text": "Hello"})

            # Make sure it redirects
            self.assertEqual(resp.status_code, 302)

            msg = Message.query.one()
            self.assertEqual(msg.text, "Hello")

            #lets test logout
            resp = c.get("/logout", follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(f'{self.testuser.username} logged out successfully', resp.get_data(as_text=True))

            #test login
            resp = c.post("/login", data={"username":"testuser2", "password":"testuser2"}, follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn(f'Hello, testuser2', resp.get_data(as_text=True))
            
            #test like
            resp = c.post(f"/users/add_like/{msg.id}")
            try:
                likes = Likes.query.one()
                pass
            except:
                self.fail("Expected a Like and there isn't one")
            
            #test unlike
            resp = c.post(f"/users/add_like/{msg.id}")
            try:
                likes = Likes.query.one()
                self.fail("Like was not deleted correctly")
            except NoResultFound:
                pass
            except MultipleResultsFound:
                self.fail("Too many likes returned")
            
            #try to delete a message with the wrong user
            resp = c.post(f"/messages/{msg.id}/delete", follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Access unauthorized", resp.get_data(as_text=True))
            

            #logout testuser2 and login testuser
            c.get("/logout", follow_redirects=True)
            resp = c.post("/login", data={"username":"testuser", "password":"testuser"}, follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn(f'Hello, testuser', resp.get_data(as_text=True))

            # ###### test delete message
            resp = c.post(f"/messages/{msg.id}/delete", follow_redirects=True)
            self.assertIn(f"@testuser", resp.get_data(as_text=True))

            # Make sure it redirects
            self.assertEqual(resp.status_code, 200)

            try:
                msg = Message.query.one()
                self.fail("NoResultFound exception should have been raised")
            except NoResultFound:
                pass
            except:
                self.fail("NoResultFound exception should have been raised, something else went wrong")

            