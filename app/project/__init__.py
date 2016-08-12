from flask import Flask, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CsrfProtect
from flask.ext.login import LoginManager, current_user
from flask.ext.heroku import Heroku
from flask.ext.principal import Identity, Principal, RoleNeed, UserNeed, Permission, identity_changed, identity_loaded

# CONFIGURATION
app = Flask(__name__) # application object
CsrfProtect(app) # enables CSRF protection for all view handlers
lm = LoginManager()
lm.init_app(app)
app.config.from_object("config.DevelopmentConfig") # read and use config file
heroku = Heroku(app)
db = SQLAlchemy(app) # sqlalchemy database object

# flask-principal
normal_role = RoleNeed('normal')
normal_permission = Permission(normal_role)
admin_role = RoleNeed('admin')
admin_permission = Permission(admin_role)
Principal(app)

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

@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
	# Set the identity user object
    identity.user = current_user

    # Add the UserNeed to the identity
    if hasattr(current_user, 'username'):
        identity.provides.add(UserNeed(current_user.username))

    # Assuming the User model has a list of roles, update the
    # identity with the roles that the user provides
    if current_user.role == 'admin':
    	identity.provides.add(normal_role)
    	identity.provides.add(admin_role)
    else:
        identity.provides.add(normal_role)
    
@app.errorhandler(403)
def need_permission(e):
	flash('You are not authorised to view that page.')
	return redirect(url_for('main.home'))