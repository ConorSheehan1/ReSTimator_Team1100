import os 

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "sample.db") # sqlite db location
SQLALCHEMY_TRACK_MODIFICATIONS = False # disabled for the time being

SECRET_KEY = "q1w2e3r4t5y6u7i8o9p0awsedrftgyhujikolpzaxscdvfbgnhmj" # used to create a cryptographoc token to validate form

RECAPTCHA_PUBLIC_KEY = '6LeYIbsSAAAAACRPIllxA7wvXjIE411PfdB2gt2J'
RECAPTCHA_PRIVATE_KEY = '6LeYIbsSAAAAAJezaIq3Ft_hSTo0YtyeFG-JgRtu'
# RECAPTCHA_API_SERVER = ? # recaptcha api server
RECAPTCHA_DATA_ATTRS = {'theme': 'dark'}