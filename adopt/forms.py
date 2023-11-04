from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, SelectField
from wtforms.validators import InputRequired, Optional, URL, Length, NumberRange


class add_pet_form(FlaskForm):
   """form for adding and updating a pet"""
   name = StringField("Pet Name", validators=[InputRequired(message="Name is Required"), Length(min=3, message="Name must be at least three characters long")])
   species = SelectField("Species", choices=["Cat", "Dog", "Porcupine"])
   photo_url = StringField("Image URL", validators=[Optional(), URL(message="Image URL must be a well-formated URL")])
   age = IntegerField("Pet age", validators=[InputRequired(message="Age is required"), NumberRange(min=0, max=30)])
   notes = StringField("Notes")
   available = BooleanField("Availability")
