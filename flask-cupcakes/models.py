"""Models for Cupcake app."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
   """connect to db"""
   db.app=app
   db.init_app(app)

class Cupcake(db.Model):
   """Cupcake model"""
   __tablename__= "cupcakes"

   id = db.Column(db.Integer, primary_key=True, autoincrement=True)
   flavor = db.Column(db.String(100), nullable=False)
   size = db.Column(db.String(10), nullable=False)
   rating = db.Column(db.Float, nullable=False)
   image = db.Column(db.String(10000), nullable=False, default="https://tinyurl.com/demo-cupcake")