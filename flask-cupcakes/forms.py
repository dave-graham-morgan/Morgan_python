from flask_wtf import FlaskForm
from wtforms import StringField, FloatField
from wtforms.validators import InputRequired


class add_cupcake_form(FlaskForm):
   """form for adding and updating a pet"""
   flavor = StringField("Pet Name", validators=[InputRequired(message="Flavor is Required")])
   size = StringField("Size", validators=[InputRequired(message="Size is a required field")])
   rating = FloatField("Rating", validators=[InputRequired(message="Rating is required")])
   image = StringField("image_url")
   