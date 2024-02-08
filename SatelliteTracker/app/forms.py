from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from .utils import US_STATES

class SignUpForm(FlaskForm):
   """form for creating a new user in the db"""
   username = StringField('Username', validators=[DataRequired()])
   email = StringField('E-mail', validators=[DataRequired(), Email(message="Must be a well-formed email address")])
   password = PasswordField('Password', validators=[Length(min=6, max=20, message="Must be between 6 and 20 characters in length")])
   confirm = PasswordField('Confirm Password', validators=[EqualTo('password', message='Does not match password'), DataRequired()])
   form_title = "Sign Up"

class LogInForm(FlaskForm):
   """form for logging in existing user"""
   username = StringField('Username', validators=[DataRequired()]) 
   password = PasswordField('Password', validators=[Length(min=6, max=20, message="Must be between 6 and 20 characters in length")])
   form_title = "Login"

class AddressForm(FlaskForm):
   """form for adding new addresses"""
   street = StringField('Street', validators=[DataRequired()])
   city = StringField('City', validators=[DataRequired()])
   state = SelectField('State', validators=[DataRequired()], choices = US_STATES)
   zip = StringField('Zip', validators=[DataRequired()])


