from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CsrfProtect
from flask.ext.login import LoginManager
from flask.ext.heroku import Heroku

# CONFIGURATION
app = Flask(__name__) # application object
CsrfProtect(app) # enables CSRF protection for all view handlers
lm = LoginManager()
lm.init_app(app)
app.config.from_object("config.DevelopmentConfig") # read and use config file
heroku = Heroku(app)
db = SQLAlchemy(app) # sqlalchemy database object
app.config['UPLOAD_FOLDER'] = './data/log_data' # This is the path to the upload directory
app.config['ALLOWED_EXTENSIONS'] = set(['zip', 'xlsx', 'csv']) # These are the extension that we are accepting to be uploaded

from project.users.views import users_blueprint
from project.analysis.views import analysis_blueprint
from project.upload.views import upload_blueprint
from project.main.views import main_blueprint

# Register blueprint
app.register_blueprint(users_blueprint)
app.register_blueprint(analysis_blueprint)
app.register_blueprint(upload_blueprint)
app.register_blueprint(main_blueprint)

from project.models import Users

lm.login_view = "users.login" # view that handles the user authentication

@lm.user_loader
def load_user(user_id):
	'''Loads user from db and stores info in the session'''
	return Users.query.filter(Users.username == user_id).first()