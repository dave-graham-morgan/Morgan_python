"""Pet adoption app"""
from flask import Flask, render_template, request, flash, redirect
from models import db, connect_db, Pet
from forms import add_pet_form
from flask_debugtoolbar import DebugToolbarExtension  

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///adopt'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "CALL-JENNY-867-5309"

#enable debugToolbar
debug = DebugToolbarExtension(app)

with app.app_context():
   connect_db(app)
   db.drop_all()
   db.create_all()
   test_pet = Pet(name="Gabe", species="dog", 
                  photo_url="https://images.unsplash.com/photo-1518717758536-85ae29035b6d?auto=format&fit=crop&q=80&w=1740&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
                  age = 3, notes="has the worst breath, but he is very sweet.  Just don't let him lick you or you will never get the smell off",
                  available = True)
   db.session.add(test_pet)
   db.session.commit()

@app.route("/")
def show_all_pets():
   pets = Pet.query.all()
   return render_template("index.html", pets=pets)

@app.route("/add", methods=["GET", "POST"])
def add_pet():
   """display adding a form and then handle adding"""
   form = add_pet_form()

   if form.validate_on_submit():
      name = form.name.data
      species = form.species.data
      photo_url = form.photo_url.data
      age = form.age.data
      notes = form.notes.data
      available = form.available.data

      new_pet = Pet(name=name, species=species,photo_url=photo_url,age=age,notes=notes,available=available)
      db.session.add(new_pet)
      db.session.commit()

      flash(f"Added {name} the {species}")
      return redirect ("/")
   else:
      return render_template("add_pet.html", form = form)
   
@app.route("/pet_details/<int:id>")
def show_pet_details(id):
   pet = Pet.query.get(id)
   if pet:
      return render_template('pet_details.html', pet=pet)

@app.route("/edit_pet/<int:id>", methods=["GET", "POST"])
def edit_pet(id):
   pet = Pet.query.get(id)
   form = add_pet_form(obj=pet)

   if form.validate_on_submit():
      pet.name = form.name.data
      pet.species = form.species.data
      pet.photo_url = form.photo_url.data
      pet.age = form.age.data
      pet.notes = form.notes.data
      pet.available = form.available.data
      db.session.commit()
      flash(f"{pet.name} updated successfully")
      return redirect("/")
   else:
      return render_template("edit_pet.html", form=form, pet=pet)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(port=8080, debug=True)
