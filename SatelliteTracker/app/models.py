"""Models for satellite tracker"""
from flask import flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy.exc import IntegrityError

bcrypt = Bcrypt()
db = SQLAlchemy()

def connect_db(app):
   """connect to db"""
   db.app=app
   db.init_app(app)
   db.create_all()
 
class User(db.Model):
   """User model"""
   __tablename__="users"

   id = db.Column(db.Integer, primary_key = True)
   username = db.Column(db.String(20), nullable=False)
   password = db.Column(db.String(61), nullable=False)
   email = db.Column(db.String(256), nullable=False)
   last_login = db.Column(db.Date)

   @classmethod
   def signup(cls, username, password, email):
      """signup a new user"""
      hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')
      
      new_user = User(
         username = username,
         email = email,
         password = hashed_pwd
      )
      db.session.add(new_user)
      
      try:
         db.session.commit()
         flash(f"{new_user.username} added successfully", "success")
      except IntegrityError:
         db.session.rollback() #remove broken user from session
         flash("Username already taken, please try again", "danger")
      except Exception as e:
         db.session.rollback()
         flash("oops... something went wrong", "danger")

      return new_user
   @classmethod
   def authenticate(cls, username, password):
      """find a user using username and password"""

      user = cls.query.filter_by(username=username).first()

      if user:
         is_authenticated_user = bcrypt.check_password_hash(user.password, password)
         if is_authenticated_user:
            return user 
      return False

class Satellite(db.Model):
   """Satellites model"""
   __tablename__ = "satellites"

   id = db.Column(db.Integer, primary_key = True)
   satcat_id = db.Column(db.Integer, nullable = False)
   last_refresh = db.Column(db.DateTime, nullable = True)
   name = db.Column(db.String(256), nullable = False)
   TLE1 = db.Column(db.String(69), nullable = True)
   TLE2 = db.Column(db.String(69), nullable = True)

class User_Satellite(db.Model):
   """users satellites join table"""
   __tablename__ = "users_satellites"

   id = db.Column(db.Integer, primary_key = True)
   user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="cascade"), nullable = False)
   satellite_id = db.Column(db.Integer, db.ForeignKey('satellites.id', ondelete="cascade"), nullable = False)
   satellite = db.relationship('Satellite', backref='user_satellites')

class Address(db.Model):
   """table for storing addresses"""
   __tablename__ = "addresses"

   id = db.Column(db.Integer, primary_key = True)
   user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="cascade"), nullable=False)
   street = db.Column(db.String(256), nullable = False)
   city = db.Column(db.String(50), nullable = False)
   state = db.Column(db.String(2), nullable = False)
   zip = db.Column(db.String(5), nullable = False)
   lat = db.Column(db.Float, nullable = True)
   lon = db.Column(db.Float, nullable = True)
   active = db.Column(db.Integer, nullable=True)

class APOD(db.Model):
   """table to store the url to the Astronomy Picture of the Day"""
   __tablename__="apods"

   id = db.Column(db.Integer, primary_key = True)
   date = db.Column(db.Date, nullable = False)
   image_url = db.Column(db.String(2083), nullable = False)
   image_json = db.Column(db.JSON, nullable = False)

class Viewing(db.Model):
   """table for storing upcoming user viewings"""
   __tablename__ = "viewings"

   id = db.Column(db.Integer, primary_key = True)
   user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="cascade"), nullable=False)
   satellite_id = db.Column(db.Integer, db.ForeignKey('satellites.id', ondelete="cascade"), nullable=False)
   address_id = db.Column(db.Integer, db.ForeignKey('addresses.id', ondelete="cascade"), nullable=False)
   satellite_name = db.Column(db.String(256), nullable = False)
   local_rise_date = db.Column(db.Date, nullable = True)
   utc_rise_time = db.Column(db.DateTime, nullable = False)
   local_rise_time = db.Column(db.DateTime, nullable = True)
   rise_direction = db.Column(db.String(3), nullable = False)
   utc_set_time = db.Column(db.DateTime, nullable = False) 
   local_set_time = db.Column(db.DateTime, nullable = True)
   set_direction = db.Column(db.String(3), nullable = False)