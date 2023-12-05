
from flask import render_template, redirect, g, session, flash, request, jsonify
from dotenv import load_dotenv
from functools import wraps
from urllib.parse import quote
from datetime import datetime, timedelta
from psycopg2 import IntegrityError
from datetime import datetime
from sqlalchemy import and_
import logging, requests, json, ephem

from .models import db, Viewing
from .utils import convert_azmith_to_ordinal, is_at_night
from config import NUM_OF_DAYS_TILL_REFRESH

def do_calculate_viewings(active_address, satellites):
   """with an active address lat and lon, refreshed satellite data (or stale from db)
   we can now calculate viewings"""
   observer = ephem.Observer()
   lat = active_address.lat
   lon = active_address.lon
   observer.lat = str(lat)
   observer.lon = str(lon)

   #set the observer time to after dark
   observer.date = observer.next_setting(ephem.Sun())
   successful_satellites = False

   #we don't want duplicate viewings at the address
   delete_previous_viewings(active_address)

   for satellite in satellites:
      #read in TLE data into ephem tracker
      ephem_satellite = ephem.readtle(satellite.name, satellite.TLE1, satellite.TLE2)

      #Want to find a viewable event or try five times
      counter = 5
      while counter > 0:
         #calculate the next pass
         next_pass = observer.next_pass(ephem_satellite)
         if next_pass:
            #extract rise time, rise direction, set time and set direction
            utc_rise_time = ephem.Date(next_pass[0])
            rise_direction = convert_azmith_to_ordinal(next_pass[1])
            utc_set_time = ephem.Date(next_pass[4])
            set_direction = convert_azmith_to_ordinal(next_pass[5])

         #create the user viewing for each satellite
         new_viewing = Viewing(user_id = g.user.id, 
                              satellite_name = satellite.name, 
                              satellite_id = satellite.id,
                              address_id = active_address.id,
                              utc_rise_time = utc_rise_time,
                              rise_direction = rise_direction,
                              utc_set_time = utc_set_time,
                              set_direction = set_direction)
         
         #check our new viewing is at night
         if is_at_night(new_viewing, observer):
            #now that we're done with our comparsion change the ephem.date objects to datetime to store. 
            new_viewing.local_rise_time = ephem.localtime(new_viewing.utc_rise_time)
            new_viewing.local_set_time = ephem.localtime(new_viewing.utc_set_time)
            new_viewing.utc_rise_time = new_viewing.utc_rise_time.datetime()
            new_viewing.utc_set_time = new_viewing.utc_set_time.datetime()
            new_viewing.local_rise_date = new_viewing.local_rise_time.date()

            db.session.add(new_viewing)  
            counter = 0
         else:
            #advance observer date to satellite set time and keep looking until we find an evening viewing
            observer.date = new_viewing.utc_set_time
            counter -= 1

   #save all new viewings
   try:
      db.session.commit() 
      return True
   except IntegrityError as e:
      db.session.rollback()
      logging.error(f"IntegrityError saving saving viewing: {str(e)}")
      return False
   except Exception as e: 
      db.session.rollback()
      logging.error(f"error writing to db from viewing route: {str(e)}")
      return False

def delete_previous_viewings(active_address):
   previous_viewings = Viewing.query.filter(
      and_(
         Viewing.address_id == active_address.id,
      )
   )
   if previous_viewings:
      previous_viewings.delete()
      try:
         db.session.commit()
      except Exception as e:
         logging.error(f"Error deleting previous viewings: {str(e)}")

def refresh_satellite_data(satellites):
   """This method will refresh satellite TLE data for those satellites whose data is more than a year old"""

   """the API does not have TLE data for every satellite, it can be unstable and the API is rate limited.
   Although TLE data will grow stale over time, especially for very low earth orbit satellites, it will only occasioinally
   alter enough within one year that satellites wont be visible to an observer as expected.  
   It is for those reasons I chose to persist TLE data and only use the API to refresh TLE data more than a year stale.  
   So we look at last_refresh date and if its older than a year we try to get up-to-date
   TLE data from the API if available or use database data we already have if not"""

   for satellite in satellites:  
      one_year_ago = (datetime.now() - timedelta(days=NUM_OF_DAYS_TILL_REFRESH)).date()
      #if we do get updated TLE, update our database with the fresher TLE data
      if satellite.last_refresh is None or satellite.last_refresh.date() < one_year_ago:
         logging.info(f"refresing TLE data for {satellite.name}")
         #for example and testing iss satcat_id is 25544 and returns a 200
         search_URL = f"https://tle.ivanstanojevic.me/api/tle/{satellite.satcat_id}"
         headers = {"User-Agent":"SatelliteTrackerApp/1.0"}
         
         resp = requests.get(search_URL, headers=headers)
         if resp.status_code == 200:
            data = resp.json()
            name = data.get("name")
            line1 = data.get("line1")
            line2 = data.get("line2")
            if name and line1 and line2:
               satellite.name = name
               satellite.TLE1 = line1
               satellite.TLE2 = line2
               satellite.last_refresh = datetime.now().date()
               db.session.add(satellite)
      else:
         logging.info("No satellite refresh needed")

   #once we're through all the satellite updates that need updating, save to db
   try:
      db.session.commit()
   except Exception as e:
      db.session.rollback()
      logging.error(f"error saving to db: {str(e)}")
      #TODO add better exceptions here.

##############################################################################
#     Helper Functions
##############################################################################
def geocode(address):
   """this function will access an external API to geocode the address (aquire lat lon)
      #free geocode api to use:
      #https://geocode.maps.co/search?street=4040+branden+ct&city=Westminster&state=CO&postalcode=80031&country=US"""
   
   #hardcoding US as this app will only work in the states (geocode limitation not satellite viewing limitation)
   search_string = f"street={address.street}&city={address.city}&state={address.state}&postalcode={address.zip}&country=US" 
   url_safe_string = quote(search_string, safe='=&',).replace('%20', '+')
   geocode = requests.get(f"https://geocode.maps.co/search?{url_safe_string}")
   
   if geocode.status_code == 200:
      data = json.loads(geocode.text)
      latitude = data[0]['lat']
      longitude = data[0]['lon']

      #check that we have a useable lat/lon (we will get a 200 for a garbage address but lat lon will be null)
      if not latitude or not longitude:
         return False
      
      address.lat = latitude
      address.lon = longitude 

   else:  #if we don't get a 200 from the API we need to return false
      return False
   
   return True

