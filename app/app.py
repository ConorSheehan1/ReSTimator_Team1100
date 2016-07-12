from flask import Flask # import Flask class
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CsrfProtect

restimatorApp = Flask(__name__) # application object
# restimatorApp.debug = True 

CsrfProtect(restimatorApp) # enables CSRF protection for all view handlers

restimatorApp.config.from_object("config.DevelopmentConfig") # read and use config file

db = SQLAlchemy(restimatorApp) # sqlalchemy database object

'''views are the handlers that respond to requests from browsers. Flask handlers are written as functions (each view function is mapped to one or more request URLs)'''
from app import views # imported after to avoid circular ref (views module needs to import the app variable)
