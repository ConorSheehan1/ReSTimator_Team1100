'''
Script used to create an app object (of class Flask).
Imports the views module.
'''
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

restimatorApp = Flask(__name__) # variable holds the Flask instance 
restimatorApp.debug = True # debugger

restimatorApp.config.from_object("config") # read and use config file

db = SQLAlchemy(restimatorApp) # sqlalchemy database object

'''views are the handlers that respond to requests from browsers. Flask handlers are written as functions (each view function is mapped to one or more request URLs)'''
from app import views#, tables #imported after to avoid circular ref (views module needs to import the app variable)
