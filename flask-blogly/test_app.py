from unittest import TestCase
from app import app
from flask import session
from models import User, db

app.config['TESTING'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False

class FlaskTests(TestCase):
   def setUp(self):
      with app.app_context():
         db.drop_all()
         db.create_all()
         user = User(first_name="Dave", last_name="Morgan", image_url="http://notanimage.pdf")
         db.session.add(user)
         db.session.commit()

      self.client = app.test_client()

   def tearDown(self):
      with app.app_context():
         db.session.rollback()

   def test_homepage(self):
      with self.client:
         res = self.client.get('/')
         html = res.get_data(as_text=True)

         self.assertEqual(res.status_code, 200)
         self.assertIn('Dave', html)
         self.assertIn('Lisa', html)