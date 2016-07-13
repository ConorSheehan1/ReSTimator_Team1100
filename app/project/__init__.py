from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CsrfProtect

###CONFIGURATION###

restimatorApp = Flask(__name__) # application object
CsrfProtect(restimatorApp) # enables CSRF protection for all view handlers
restimatorApp.config.from_object("config.DevelopmentConfig") # read and use config file
db = SQLAlchemy(restimatorApp) # sqlalchemy database object

###VIEWS: handlers that respond to requests from browsers. Flask handlers are written as functions (each view function is mapped to one or more request URLs)###
# from sign_up import RegistrationForm
# from analysis import AnalysisForm

from project.users.views import users_blueprint
from project.main.views import main_blueprint

# # Register blueprint
restimatorApp.register_blueprint(users_blueprint)
restimatorApp.register_blueprint(main_blueprint)