from flask import redirect, url_for, flash, request, g, render_template,session
from functools import wraps
from config import CURR_USER_KEY
import math, ephem

US_STATES = [
   ('AL', 'Alabama'), ('AK', 'Alaska'), ('AZ', 'Arizona'), ('AR', 'Arkansas'),
   ('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DE', 'Delaware'),
   ('FL', 'Florida'), ('GA', 'Georgia'), ('HI', 'Hawaii'), ('ID', 'Idaho'),
   ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'),
   ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MD', 'Maryland'),
   ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'),
   ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'),
   ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'),
   ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('OH', 'Ohio'), ('OK', 'Oklahoma'),
   ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'),
   ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'),
   ('VT', 'Vermont'), ('VA', 'Virginia'), ('WA', 'Washington'), ('DC', 'Washington DC'),
   ('WV', 'West Virginia'), ('WI', 'Wisconsin'), ('WY', 'Wyoming')
   ]

##############################################################################
#     helpers                                                                #
##############################################################################
def login_required(f):
    """this function used to decorate a route that requires login
    if the user is not logged in system will redirect to login page and
    after login, user will be taken back to the page they were accessing"""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not g.user:
            flash("Please log in or sign up to view that page", "danger")
            return redirect(url_for('auth.log_user_in', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def do_login(user):
   """Log in user."""
   session[CURR_USER_KEY] = user.id

def do_logout():
   """Log out user"""
   if CURR_USER_KEY in session:
      del session[CURR_USER_KEY]

def convert_azmith_to_ordinal(azimuth_angle):
    """this function will take an azimuth and convert that into
    a human readable ordinal directions"""

    azimuth_degrees = math.degrees(azimuth_angle)
    azimuth_direction = compass_direction(azimuth_degrees)
    return azimuth_direction

def compass_direction(degrees):
    """helper function that takes degree and converts to ordinal"""
    directions = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
    index = round(degrees / 22.5) % 16
    return directions[index]

def is_at_night(viewing, observer):
    """this helper function will determine whether the viewing will be
    after sunset and before sunrise at the observer's location"""
    
    #create a deep copy of observer so that we leave original observer object pristine 
    local_observer = ephem.Observer()
    local_observer.lat = observer.lat
    local_observer.lon = observer.lon
    local_observer.date = viewing.utc_rise_time
    local_observer.pressure = 0

    # horizon of '-18' corresponds to astronomical twilight (fully dark)
    # it also means any satellite transit of any duration will be dark enough to view in its entirety
    local_observer.horizon = '-18' 

    utc_sunrise = local_observer.previous_rising(ephem.Sun())
    utc_sunset = local_observer.next_setting(ephem.Sun())

    utc_sunset_time = utc_sunset.datetime().time()
    utc_sunrise_time = utc_sunrise.datetime().time()
    utc_rise_time = viewing.utc_rise_time.datetime().time()

    if utc_sunset_time < utc_rise_time < utc_sunrise_time:
        return True
    else:
        return False
