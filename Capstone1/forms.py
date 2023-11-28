from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField #, TextAreaField
from wtforms.validators import DataRequired, Email, Length, EqualTo
# from wtforms.widgets import TextArea


class SignUpForm(FlaskForm):
   """form for creating a new user in the db"""
   username = StringField('Username', validators=[DataRequired()])
   email = StringField('E-mail', validators=[DataRequired(), Email(message="Must be a well-formed email address")])
   password = PasswordField('Password', validators=[Length(min=6, max=20, message="Must be between 6 and 20 characters in length")])
   confirm = PasswordField('Confirm Password', validators=[EqualTo('password', message='Does not match password'), DataRequired()])

