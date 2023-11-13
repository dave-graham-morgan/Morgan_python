from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, TextAreaField
from wtforms.validators import InputRequired

class regsiter_user_form(FlaskForm):
   """form for registering a new user"""
   username = StringField("Username", validators=[InputRequired(message="Username is required")])
   password = PasswordField("Password", validators=[InputRequired(message="Password is required")])
   email = EmailField("Email", validators=[InputRequired(message="Email is required")])
   first_name = StringField("First Name", validators=[InputRequired(message="A first name is required")])
   last_name = StringField("Last Name", validators=[InputRequired(message="A last name is required")])



class login_form(FlaskForm):
   """form for logging in an existing user"""
   username = StringField("Username", validators=[InputRequired(message="Username is required")])
   password = PasswordField("Password", validators=[InputRequired(message="Password is required")])

class feedback_form(FlaskForm):
   """form for feedback"""
   title = StringField("Title", validators=[InputRequired(message="You must enter a title")])
   content = TextAreaField("Content", validators=[InputRequired(message="Content is required duh")])
