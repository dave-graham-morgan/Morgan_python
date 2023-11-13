"""Flask app for auth app"""
from flask import Flask, render_template,redirect, flash, request, session
from flask_bcrypt import Bcrypt
from flask_wtf import FlaskForm
from models import db, connect_db, User, Feedback
from forms import regsiter_user_form, login_form, feedback_form
from sqlalchemy.exc import IntegrityError

#from flask_debugtoolbar import DebugToolbarExtensions

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///auth'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "CALL-JENNY-867-5309"

with app.app_context():
   connect_db(app)
   db.drop_all()
   db.create_all()
   
   # add sample user
   seed_user = User(username="dave", password="$2b$12$FswxiXNSIZyGnj4E/zC.3.Xk7Oy36uGCrTnwOVJ2swP5vUbkCgZq6",
                   email="dave.g.morga@and.gmail", first_name="Dave", last_name="Morgan")
   db.session.add(seed_user)
   try:
      db.session.commit()
   except Exception as e:
      print("database exception error" + e)
   

@app.route("/")
def index():
   all_users = User.query.all()
   return render_template("index.html", users = all_users)

@app.route("/register", methods=['GET', 'POST'])
def register():
   form = regsiter_user_form()

   if form.validate_on_submit():
      
      username = form.username.data
      password = form.password.data
      email = form.email.data
      first_name = form.first_name.data
      last_name = form.last_name.data

      bcrypt = Bcrypt()
      hash = bcrypt.generate_password_hash(password)
      hashed_password = hash.decode("utf-8")

      new_user = User(username = username, password=hashed_password, email=email, first_name = first_name, last_name=last_name)
      db.session.add(new_user)
      try:
         db.session.commit()
         flash(f"User first name: {first_name}, last name: {last_name} added successfully", "success")
         session['username'] = new_user.username
         return redirect("/users/{{new_user.username}}")
      except IntegrityError:
         flash(f"that username has been taken, try another", "danger")
         return render_template("/register.html",form=form)
      except:
         flash("something bad happened")
         return render_template("/register.html", form=form)
      
   else:
      return render_template("/register.html", form=form)
   

@app.route("/secret")
def show_secret():
   if session.get('username'):
      return render_template("secret.html")
   else:
      return redirect('/login')

@app.route("/login", methods=["GET", "POST"])
def login_user():
   form = login_form()
   if form.validate_on_submit():
      username = form.username.data
      password = form.password.data
      user = None
      try:
         user = User.query.filter(User.username==username).first()
      except:
         flash("Something bad happened", "danger")
         return redirect("/")
      
      if user:
         bcrypt = Bcrypt()
         if bcrypt.check_password_hash(user.password, password):
            flash(f"{username} logged in successfully", "success")
            session['username'] = user.username
            
            return redirect(f"/users/{username}")
         else:
            flash(f"Invalid username/password", "danger")       

      else:
         flash(f"Invalid username/password", "danger") 
      
      return redirect("/")
   else:
      return render_template("login.html", form=form)
   
@app.route("/logout")
def logout():
   session.pop('username', None)
   return redirect ('/')

@app.route("/users/<username>")
def show_user(username):
   user = User.query.filter(User.username == username).first()
   feedback = Feedback.query.filter(Feedback.username == username)

   if user:
      return render_template("user_details.html", user=user, feedback=feedback)
   else:
      return redirect('/')

@app.route("/feedback/<int:id>")
def show_feedback(id):
   feedback = Feedback.query.get(id)
   form = feedback_form()
   form.title.data = feedback.title
   form.content.data = feedback.content
   user = feedback.author
   return render_template("feedback.html", feedback=feedback, form=form, user=user)

@app.route("/feedback/<int:id>/update", methods=["POST"])
def update_feedback(id):
   feedback = Feedback.query.get(id)
   new_title = request.form['title']
   new_content = request.form['content']
   feedback.title = new_title
   feedback.content = new_content
   db.session.add(feedback)
   try:
      db.session.commit()
   except Exception as e:
      print("problems writing to db")
      print(e)
   return redirect(f"/users/{feedback.username}")

@app.route("/users/<username>/feedback/add", methods=["GET","POST"])
def add_feedback(username):
   form = feedback_form()
   user = User.query.get(username)

   if form.validate_on_submit():
      title = form.title.data
      content = form.content.data
      new_feedback = Feedback(title=title, content=content, username=username)
      db.session.add(new_feedback)
      try:
         db.session.commit()
      except Exception as e:
         print("*** error writing to database ***")
         print(e)
         return redirect("/")
      return redirect("/users/{{user.username}}")
   else:
      return render_template("add_feedback.html", form=form, user=user)


@app.errorhandler(404)
def page_not_found(error):
   return render_template('404.html'), 404

if __name__ == '__main__':
   app.run(port=8080, debug=True)