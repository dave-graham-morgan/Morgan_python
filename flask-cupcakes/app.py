"""Flask app for Cupcakes"""
from flask import Flask, make_response, render_template, request,jsonify
from flask_wtf import FlaskForm
from models import db, connect_db, Cupcake
from forms import add_cupcake_form
from seed import c1, c2
#from flask_debugtoolbar import DebugToolbarExtensions

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "CALL-JENNY-867-5309"


with app.app_context():
   connect_db(app)
   db.drop_all()
   db.create_all()
   db.session.add_all([c1, c2])
   db.session.commit()

@app.route("/")
def display_list_page():
   return render_template("index.html")

@app.route("/api/cupcakes")
def get_all_cupcakes():
   cupcakes = Cupcake.query.all()
   serilized = [serialize(cupcake) for cupcake in cupcakes]
   return jsonify(cupcakes=serilized)

@app.route("/api/cupcakes/<int:id>")
def get_a_cupcake(id):
   cupcake = Cupcake.query.get(id)
   serilized = serialize(cupcake)
   return jsonify(cupcake=serilized)  #TODO return JSON

@app.route("/api/cupcakes", methods=["POST"])
def create_new_cupcake():
   data = request.get_json()

   #i'm just going to check this simply this round. I will use flask-wtf going forward for request validation
   if data.get("flavor") and data.get('size') and data.get('rating') and data.get('image'):
      flavor = data.get("flavor")
      size = data.get('size')
      rating = data.get('rating')
      image = data.get('image')

   new_cupcake = Cupcake(flavor = flavor, size=size, rating=rating,image=image)
   db.session.add(new_cupcake)
   #put this in try catch do this for anything external
   try:
      db.session.commit()
   except Exception as e:
      print("Exception occured writing to db")
      print(e)
   reponse = make_response(jsonify(cupcake=serialize(new_cupcake)), 201)
   return reponse

@app.route("/api/cupcakes/<int:id>", methods=["PATCH"])
def update_cupcake(id):
   cupcake = Cupcake.query.get_or_404(id)
   data = request.get_json().get('cupcake')

   cupcake.flavor = data.get("flavor")
   cupcake.size = data.get("size")
   cupcake.rating = data.get("rating")
   cupcake.image = data.get("image")

   db.session.add(cupcake)
   db.session.commit()  ##try catch

   return jsonify(cupcake=serialize(cupcake))

@app.route("/api/cupcakes/<int:id>", methods=["DELETE"])
def delete_cupcake(id):
   cupcake = Cupcake.query.get_or_404(id)
   db.session.delete(cupcake)
   db.session.commit()
   return jsonify(message="Deleted")

def serialize(cupcake):
   return{"id":cupcake.id,
          "flavor": cupcake.flavor,
          "size": cupcake.size,
          "rating": cupcake.rating,
          "image":cupcake.image
         }

@app.errorhandler(404)
def page_not_found(error):
   return render_template('404.html'), 404

if __name__ == '__main__':
   app.run(port=8080, debug=True)