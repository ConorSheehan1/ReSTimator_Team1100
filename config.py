import os 

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "data.db")
SQLALCHEMY_TRACK_MODIFICATIONS = False

WTF_CSRF_ENABLED = True	# cross-site request forgery protection enabled to make application more secure (READ UP ON)
SECRET_KEY = "q1w2e3r4t5y6u7i8o9p0awsedrftgyhujikolpzaxscdvfbgnhmj" # used to create a cryptographoc token to validate form