"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
   """connect to db""" 

   db.app=app
   db.init_app(app)

class User(db.Model):
   """User"""
   __tablename__ = "users"

   id = db.Column(db.Integer,
                  primary_key = True,
                  autoincrement=True)
   first_name = db.Column(db.String(50), 
                  nullable = False,
                  unique = False)
   last_name = db.Column(db.String(50), 
                  nullable = False,
                  unique = False)
   image_url = db.Column(db.String(10000),
                  nullable = True,
                  unique = False)
   posts = db.relationship('Post', backref='author') #lazy=True
                           

class Post(db.Model):
   """one to many posts to users"""
   __tablename__ = "posts"
   id = db.Column(db.Integer,
                  primary_key = True,
                  autoincrement=True)
   title = db.Column(db.String(300), nullable = False)
   content = db.Column(db.String(10000))
   user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
   tags = db.relationship('Tag', secondary='post_tags', backref=db.backref('posts'))
   
class Tag(db.Model):
   """many to many posts to users"""
   __tablename__ = "tags"
   id = db.Column(db.Integer, primary_key = True, autoincrement=True)
   name = db.Column(db.String(300), nullable=False) 
   #posts = db.relationship('Post', secondary='post_tags', backref=db.backref('tags'))

class PostTag(db.Model):
   """join table for Tag and Post"""
   __tablename__="post_tags"
   post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
   tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)

   
