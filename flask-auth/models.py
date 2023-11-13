"""Models for auth app."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
   """connect to db"""
   db.app=app
   db.init_app(app)

class User(db.Model):
   """User model"""
   __tablename__="users"

   username = db.Column(db.String(20), primary_key=True)
   password = db.Column(db.String(1000), nullable=False)
   email = db.Column(db.String(50), nullable=False)
   first_name = db.Column(db.String(30), nullable=False)
   last_name = db.Column(db.String(30), nullable=False)
   feedback = db.relationship('Feedback', backref='author')

class Feedback(db.Model):
   """feedback model"""
   __tablename__ = "feedback"

   id = db.Column(db.Integer, primary_key=True, autoincrement=True)
   title = db.Column(db.String(20), nullable=False)
   content = db.Column(db.String(1000), nullable=False)
   username = db.Column(db.String(20), db.ForeignKey('users.username'), nullable=False)