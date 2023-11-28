"""Models for satellite tracker"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
   """connect to db"""
   db.app=app
   db.init_app(app)

class User(db.Model):
   """User model"""
   __tablename__="users"

   id = db.Column(db.Integer, primary_key = True)
   username = db.Column(db.String(20), nullable=False)
   password = db.Column(db.String(61), nullable=False)
   email = db.Column(db.String(256), nullable=False)
   last_login = db.Column(db.Date)

class Satellite(db.Model):
   """Satellites model"""
   __tablename__ = "satellites"

   id = db.Column(db.Integer, primary_key = True)
   satcat_id = db.Column(db.Integer, nullable = False)
   name = db.Column(db.String(256), nullable = False)
   TLE1 = db.Column(db.String(69), nullable = True)
   TLE2 = db.Column(db.String(69), nullable = True)

class User_Satellite(db.Model):
   """users satellites join table"""
   __tablename__ = "users_satellites"

   id = db.Column(db.Integer, primary_key = True)
   user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="cascade"))
   satellite_id = db.Column(db.Integer, db.ForeignKey('satellites.id', ondelete="cascade"))

class Address(db.Model):
   """table for storing addresses"""
   __tablename__ = "addresses"

   id = db.Column(db.Integer, primary_key = True)
   user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="cascade"))
   street_number = db.Column(db.String(256),nullable = False)
   street = db.Column(db.String(256), nullable = False)
   city = db.Column(db.String(50), nullable = False)
   state = db.Column(db.String(2), nullable = False)
   zip = db.Column(db.String(5), nullable = False)
   zip_plus_4 = db.Column(db.String(4), nullable = True)
   lat = db.Column(db.Float, nullable = True)
   long = db.Column(db.Float, nullable = True)