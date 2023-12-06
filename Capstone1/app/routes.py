from flask import  render_template, redirect, g, flash, request, jsonify, Blueprint, Response
from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from datetime import date
import logging, os, requests

from .models import db, User, Satellite, User_Satellite, Address, Viewing, APOD
from .forms import SignUpForm, LogInForm, AddressForm
from .utils import login_required, do_login, do_logout
from .services import refresh_satellite_data, do_calculate_viewings, geocode

##############################################################################
#     User signup/login/logout
##############################################################################
auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route("/sign_up", methods=["GET", "POST"])
def display_signup():
   """handle user signup and add new users to db"""
   form = SignUpForm()

   if form.validate_on_submit():
      user = User.query.filter_by(username=form.username.data).first()

      if user:
         flash(f"username: {form.username.data}, has already been taken.  Try a different username.", "danger")
         return redirect("/sign_up")
     
      new_user = User.signup(
         username = form.username.data,
         password = form.password.data,
         email = form.email.data
      )
      do_login(new_user)
      return redirect("/user_details")

   else:
      return render_template("sign_up.html", form = form)
   
@auth_blueprint.route("/logout")
def log_user_out():
   do_logout()
   return redirect("/")

@auth_blueprint.route("/login", methods=["GET", "POST"])
def log_user_in():
   next_url = request.args.get('next')
   form = LogInForm()   
   print(request.method)
   print("form errors:")
   print(form.errors)
   print(f"next_url: {next_url}")
   print(f"form username: {form.username.data}")
   print(f"form password: {form.password.data}")
   if form.validate_on_submit():
      user = User.authenticate(form.username.data, form.password.data)
      if user:
         do_login(user)
         flash(f"Welcome back {user.username}!", "success")
         if next_url:
            return redirect(next_url)
         else:
            return redirect("/user_details")
      else:
         flash(f"Invalid username/password combination, try again or sign up", "danger")
         return redirect("/login")
   return render_template("login.html", form=form)



##############################################################################
#     Addresses / satellite details
##############################################################################
user_details_blueprint = Blueprint('user_details', __name__)

@user_details_blueprint.route("/add_satellite", methods=["POST"])
@login_required
def add_user_satellite():
   """this method will add records to users_satellite join table"""
   data = request.json
   satellite_id = data.get('satelliteId')
   user_id = g.user.id

   new_user_satellite = User_Satellite(satellite_id = satellite_id, user_id = user_id)
   db.session.add(new_user_satellite)
   try:
      db.session.commit() 
      return jsonify({"message": "success"}),200
   except IntegrityError as e:
      logging.error(f"integrityError saving saving user_satellite: {str(e)}")

   except Exception as e:
      logging.error(f"error writing to db from add_satellite route: {str(e)}")
      return jsonify({"message":"error"},500)

@user_details_blueprint.route("/remove_satellite", methods=["POST"])
@login_required
def remove_user_satellite():
   """this method will remove a record from users_satellite join table"""
   data = request.json
   satellite_id = data.get('satelliteId')
   user_id = g.user.id

   satellite_to_delete = User_Satellite.query.filter_by(user_id=user_id, satellite_id=satellite_id).first()
   if satellite_to_delete:
      db.session.delete(satellite_to_delete)
      try:
         db.session.commit()
         return jsonify({"success": "Satellite removed successfully"}, 200)
      except IntegrityError as e:
         db.session.rollback()
         logging.error(f"IntegrityError saving user_satellite: {str(e)}")
      except Exception as e:
         db.session.rollback()
         logging.error(f"Error: {str(e)}")
         return jsonify({"error": "Error removing satellite"}, 500)
   return jsonify({"error": "Error removing satellite"}, 500) 


@user_details_blueprint.route("/get_user_satellites", methods=["GET"])
@login_required
def get_user_satellites():
   """this route will pass user satellite data to the user_details page upon load"""
   user_satellites = User_Satellite.query.filter_by(user_id=g.user.id).all()
   satellite_ids = [us.satellite_id for us in user_satellites]
   return jsonify(satellite_ids)

@user_details_blueprint.route("/add_address", methods=["POST"])
def add_address():
   """this method will add an address to the db"""
   data = request.json
   user_id = g.user.id
   street = data.get('street')
   city = data.get('city')
   state = data.get('state')
   zip = data.get('zip')
   new_address = Address(user_id=user_id,
                         street = street,
                         city = city,
                         state=state,
                         zip=zip)
   
   #check that the address can be geocoded
   if not geocode(new_address):
      return jsonify({"error": "Unable to geocode address"}, 500)
   
   #we have everything we need to attept to save the address
   db.session.add(new_address)

   try:
      db.session.commit()
      new_address_id = new_address.id
      return jsonify({"success": "Address added successfully", "address_id": f"{new_address_id}"}, 201)
   except IntegrityError as e:
      db.session.rollback()
      logging.error(f"IntegrityError: {str(e)}")
      return jsonify({"error": "Unable to add address due to integrity constraint"}, 500)
   except Exception as e:
      db.session.rollback()
      logging.error(f"Error: {str(e)}")
      return jsonify({"error": "Unable to add address"}, 500)

@user_details_blueprint.route("/remove_address", methods=["POST"])
def remove_address():
   """this method will remove an address from the db"""
   data = request.json
   address_id = data.get('addressId')
   address_to_delete = Address.query.get(address_id)
   db.session.delete(address_to_delete)

   try:
      db.session.commit()
      return jsonify({"success": "Address removed successfully"}, 200)
   except IntegrityError as e:
      db.session.rollback()
      logging.error(f"IntegrityError: {str(e)}")
      return jsonify({"error": "Unable to remove address due to integrity constraint"}, 500)
   except Exception as e:
      db.session.rollback()
      logging.error(f"Error: {str(e)}")
      return jsonify({"error": "Unable to remove address"}, 500)
   
@user_details_blueprint.route("/make_address_active", methods=["POST"])
def make_address_active():
   data = request.json
   address_id = data.get('addressId')
   user_id = g.user.id
   newly_active_address = Address.query.get(address_id)
   
   previously_active_address = Address.query.filter(and_(
      Address.user_id == user_id,
      Address.active == 1
   )).first()

   if previously_active_address:
      previously_active_address.active = 0
      db.session.add(previously_active_address)
   
   newly_active_address.active = 1
   db.session.add(newly_active_address)
 
   
   try:
      db.session.commit()
      return jsonify({"success": "Address successfully made active"}, 200)
   except IntegrityError as e:
      db.session.rollback()
      logging.error(f"IntegrityError: {str(e)}")
      return jsonify({"error": "Unable to promote address due to integrity constraint"}, 500)
   except Exception as e:
      db.session.rollback()
      logging.error(f"Error: {str(e)}")
      return jsonify({"error": "Unable to promote address"}, 500)

@user_details_blueprint.route("/user_details")
@login_required
def user_details_page():
   """this route will display the user-details page which includes satellites, addresses and viewings"""
   address_form =  AddressForm()
   satellites = db.session.query(Satellite)
   addresses = Address.query.filter_by(user_id = g.user.id).all()
   return render_template("user_details.html", 
                          satellites = satellites, 
                          addresses = addresses, 
                          address_form = address_form)

##############################################################################
#     Homepage
##############################################################################
homepage_blueprint = Blueprint('homepage_blueprint', __name__)

@homepage_blueprint.route("/")
def display_homepage():
   if g.user:
      return redirect("/user_details")
   else:
      return render_template("index.html")

@homepage_blueprint.route("/get_apod")
def get_apod():
   """function to get the astronomy picture of the day from NASA and persist its data.
   this is done to enhance performance as well as keep from being throttled by NASA as this should
   call just once per day app-wide as opposed to once per homepage load. Keep in mind there is also
   a default image if we do not get a response from the API"""

   #check if we already have today's photo of the day
   today = date.today()
   today_photo = APOD.query.filter_by(date = today).first()

   if today_photo:
      return Response(today_photo.image_json, content_type ='application/json')
   else:
      apod = requests.get(f"https://api.nasa.gov/planetary/apod?api_key={os.environ.get('NASA_API_KEY')}")
      data = apod.json()
      new_photo = APOD(date = today, image_url = data.get("url"), image_json = apod.text)
      db.session.add(new_photo)
      db.session.commit()

      # new_photo = APOD(date = today, image_url = )
      return Response(apod.text, content_type = 'application/json')
 
##############################################################################
#     Viewings
##############################################################################
@user_details_blueprint.route("/get_viewings", methods=["GET"])
@login_required
def calculate_viewings():
   """this method will calculate and return viewings"""
   
   active_address = Address()
   #first we need to verify we have an active address 
   try:
      active_address = Address.query.filter(and_(
      Address.user_id == g.user.id,
      Address.active == 1
      )).one()
      
   except NoResultFound:
      return jsonify({"error": "You must have at least one active address"}, 400)
   except MultipleResultsFound:
      logging.error(f"Data integrity error, multiple active addresses found.")
      return jsonify({"error":"Multiple active addresses found"}, 500)
   
   #we also need to get the satellites the user is tracking
   user_satellites = User_Satellite.query.filter(User_Satellite.user_id == g.user.id).all()
   satellite_ids = [user_satellite.satellite_id for user_satellite in user_satellites]
   satellites = Satellite.query.filter(Satellite.id.in_(satellite_ids)).all()

   refresh_satellite_data(satellites)
   has_viewings = do_calculate_viewings(active_address, satellites)
   if has_viewings:
      viewings = Viewing.query.filter(
                  Viewing.user_id == g.user.id, 
                  Viewing.address_id == active_address.id
                  ).order_by(Viewing.local_rise_time).all()
      dict_viewings = []
      for viewing in viewings:
         duration = viewing.local_set_time - viewing.local_rise_time
         duration_in_minutes = int(round(duration.total_seconds()/60, 0))
         viewing_data = {
            "satellite": viewing.satellite_name,
            "date": str(viewing.local_rise_date),
            "visible": str(duration_in_minutes) + "min",
            "rise": str(viewing.local_rise_time.strftime('%I:%M %p')),
            "appears": viewing.rise_direction,
            "dissappears": viewing.set_direction
         }
         dict_viewings.append(viewing_data)
      response_data = {
         "address": active_address.street,
         "viewings":dict_viewings
      }   
      return jsonify(response_data)
   
   #no viewings for the active address and selected satellites
   else: 
      response_data = {
      "address":active_address.street,
      "viewings":"None"
   }
      return jsonify(response_data)







