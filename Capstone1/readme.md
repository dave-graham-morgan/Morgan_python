
Welcome to Satellite tracker!  Satellite tracker will allow you to enter in an address or lat long and select a number of satellites.
Once you set an address and select at least one satellite, the system will calculate a number of upcomming 'viewings' where you will be able to see the selected satelit(s) transit your location. 

Light pollution and weather at your location may make some satellites difficult or impossible to see.  Some satellites may not be visibile during the evening at your lattitude. Brightest satellites are bluewalker 3 and the ISS which are both available to track and visibile throughout much of the United Statees and so they a good place to start. 

To get started clone repo and built venv from requirements.txt.
create a .env file based on the .env.example file. 
create a postgreSQL database and call it satellite_tracker. Add the URI to the .env file
run the seed_sats.py file to seed the database with the brightest satellites (as of Dec 2023)

A NASA api key is required to view the astronomy picture of the day on the homepage (otherwise a default image will dispaly).  To secure a NASA api key go to: https://api.nasa.gov/ and add that API key to your .env file. 

Technology used in the making of this site includes:
-flask
-wtforms
-flask-sqlalchemy
-bcrypt
-jQuery
-ajax
-pyephem (for calculating satellite transits) 

Api's used:
-Nasa Astronomy Photograph of the Day (APOD) (requries a free key)
-https://tle.ivanstanojevic.me/api for refreshing satellite TLE data
-geocode.maps for geocoding addresss (free - rate limited, throttled)



