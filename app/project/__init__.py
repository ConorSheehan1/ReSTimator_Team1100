from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CsrfProtect
from flask.ext.login import LoginManager

# CONFIGURATION
restimatorApp = Flask(__name__) # application object
CsrfProtect(restimatorApp) # enables CSRF protection for all view handlers
lm = LoginManager()
lm.init_app(restimatorApp)
restimatorApp.config.from_object("config.DevelopmentConfig") # read and use config file
db = SQLAlchemy(restimatorApp) # sqlalchemy database object

from project.users.views import users_blueprint
from project.main.views import main_blueprint

# Register blueprint
restimatorApp.register_blueprint(users_blueprint)
restimatorApp.register_blueprint(main_blueprint)

from project.models import Users

lm.login_view = "users.login" # view that handles the user authentication

@lm.user_loader
def load_user(user_id):
	'''Loads user from db and stores info in the session'''
	return Users.query.filter(Users.username == user_id).first()