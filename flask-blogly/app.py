"""Blogly application."""

from flask import Flask, render_template, session, request,jsonify, flash, redirect, url_for
from models import db, connect_db, User
from flask_debugtoolbar import DebugToolbarExtension  

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "CALL-JENNY-867-5309"

# enable debugToolbar
debug = DebugToolbarExtension(app) #i'm getting a weird error when trying to import debugtoolbar! 



with app.app_context():
   connect_db(app)
   db.drop_all()
   db.create_all()

@app.route("/")
def show_users():
    all_users = User.query.all()
    return render_template("users.html", all_users = all_users)

@app.route("/new_user")
def create_new_user():
   return render_template("new_user.html")


@app.route("/add_user", methods=["POST"])
def add_user_():
   first_name = request.form['first_name']
   last_name = request.form['last_name']
   image_url = request.form['image_url']
   
   new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
   db.session.add(new_user)
   db.session.commit()

   return redirect ("/")

@app.route("/user_details/<int:id>")
def show_user_details(id):
   user = User.query.filter(User.id == id).first()

   return render_template("user_details.html", user=user)


@app.route("/edit_user/<int:id>")
def edit_user(id):
   user = User.query.filter(User.id == id).first()
   return render_template("edit_user.html", user=user)

@app.route("/update_user/<int:id>", methods=["POST"])
def update_user(id):
   user = User.query.get(id)
   if(user):
      user.first_name = request.form['first_name']
      user.last_name = request.form['last_name']
      user.image_url = request.form['image_url']
      db.session.commit()
      return redirect (f'/user_details/{id}')
   
@app.route("/delete_user/<int:id>")
def delete_user(id):
   user = User.query.get(id)
   if(user):
      db.session.delete(user)
      db.session.commit()
      return redirect('/')

if __name__ == '__main__':
    app.run(port=8080, debug=True)
