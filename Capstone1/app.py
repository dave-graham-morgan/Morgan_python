from flask import Flask, render_template, redirect, g, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from dotenv import load_dotenv
from sqlalchemy.exc import IntegrityError
import os

from models import db, connect_db, User, Satellite, User_Satellite
from forms import SignUpForm

app = Flask(__name__)

load_dotenv() #this will load settings from the .env file into the os
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CURR_USER_KEY = "initialize_me"

connect_db(app)

if os.environ.get('ENVIRONMENT') == 'DEV':
   db.drop_all()
   db.create_all()
   app.config['WTF_CSRF_ENABLED'] = False
   app.config['SQLALCHEMY_ECHO'] = True
   app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
   toolbar = DebugToolbarExtension(app)
   
else:
   db.create_all()
   app.config['WTF_CSRF_ENABLED'] = True
   app.config['SQLALCHEMY_ECHO'] = False
   app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


@app.route("/")
def display_homepage():
   print("normally we'd see a homepage")
   return render_template('index.html')



@app.route("/sign_up", methods=["GET", "POST"])
def display_signup():
   """handle user signup and add new users to db"""
   form = SignUpForm()

   if form.validate_on_submit():
     
      new_user = User.signup(
         username = form.username.data,
         password = form.password.data,
         email = form.email.data
      )
      
      try:
         db.session.commit()
         flash(f"{new_user.username} added successfully", "success")
      except IntegrityError:
         db.session.rollback() #remove broken user from session
         flash("Username already taken, please try again", "danger")
      except Exception as e:
         db.session.rollback()
         flash("oops... something went wrong", "danger")
         print(e)




@app.errorhandler(404)
def page_not_found(error):
   return render_template('404.html'), 404

if __name__ == '__main__':
   app.run(port=8080, debug=True)