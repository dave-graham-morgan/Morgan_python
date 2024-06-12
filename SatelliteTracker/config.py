from dotenv import load_dotenv
import os


CURR_USER_KEY = "initialize_me"
try:
   NUM_OF_DAYS_TILL_REFRESH = int(os.environ.get('NUM_OF_DAYS_TILL_REFRESH'))
except:
   #if we can't cast to a number, default to one year
   NUM_OF_DAYS_TILL_REFRESH = 365

class ConfigDev():
   load_dotenv() #this will load settings from the .env file into the os
   SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DEV_DATABASE_URI')
   SECRET_KEY = os.environ.get('DEV_SECRET_KEY')
   SQLALCHEMY_TRACK_MODIFICATIONS = False
   WTF_CSRF_ENABLED = True  #better to leave on even in dev to ensure it works
   SQLALCHEMY_ECHO = False  #toggle depending on the need
   DEBUG_TB_INTERCEPT_REDIRECTS = False

class Config():
   load_dotenv()
   SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_PROD_DATABASE_URI')
   SECRET_KEY = os.environ.get('PROD_SECRET_KEY')
   SQLALCHEMY_TRACK_MODIFICATIONS = False
   WTF_CSRF_ENABLED = True
   SQLALCHEMY_ECHO = False
   DEBUG_TB_INTERCEPT_REDIRECTS = False 


