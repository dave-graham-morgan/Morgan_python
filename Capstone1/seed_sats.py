"""Seed satellite database with the brightest satellites viewable in US."""

import csv, os
from app import db
from models import Satellite, Address, User

db.drop_all()
db.create_all()

with open('data/satellites.csv') as satellites:
   reader = csv.reader(satellites)
   data = list(reader)

for i in range(0, len(data), 3):
   name = data[i][0]
   tle1 = data[i+1][0]
   tle2 = data[i+2][0] 
   satellite_id = int(tle2[2:8].strip()) #extract digits 2 - 8, strip white spaces and convert to int

   new_satellite = Satellite(name = name, satcat_id = satellite_id, TLE1 = tle1, TLE2 = tle2)
   db.session.add(new_satellite)
   try:
      db.session.commit()
   except:
      db.session.rollback()

#seed user and addresses in Dev only
if os.environ.get('ENVIRONMENT') == 'DEV':
   new_user = User(id=1, username='dave', password='$2b$12$I/bm6hUomU4YQgVPP7ImA.NhlwlwUD.hK2CLqzlvWIlzmNGznzbtq', email='notemail@nowhere.com')
   db.session.add(new_user)
   try:
      db.session.commit()
   except:
      db.session.rollback()


   new_address1 = Address(user_id=1, street_number = 350, street = "Fifth Avenue", city="New York City", state="NY", zip="10118", active=1)
   db.session.add(new_address1)
   new_address2 = Address(user_id=1, street_number = 1600, street = "Pennsylvania Avenue", city="Washington DC", state="DC", zip="20500", active=0)
   db.session.add(new_address2)
   try:
      db.session.commit()
   except:
      db.session.rollback()