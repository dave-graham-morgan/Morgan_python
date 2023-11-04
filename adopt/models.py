"""Models for Adopt"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
   """connect to db"""

   db.app=app
   db.init_app(app)

class Pet(db.Model):
   """class for our Pet model"""
   __tablename__ = "pets"
   id = db.Column(db.Integer, primary_key = True, autoincrement=True)
   name = db.Column(db.String(50), nullable=False)
   species = db.Column(db.String(50), nullable=False)
   photo_url = db.Column(db.String(10000), nullable=True)
   age = db.Column(db.Integer, nullable=True)
   notes = db.Column(db.String(10000), nullable=True)
   available = db.Column(db.Boolean, nullable=False, default=True )

