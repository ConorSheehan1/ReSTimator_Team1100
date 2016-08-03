import os 


class BaseConfig():
	''''''
	basedir = os.path.abspath(os.path.dirname(__file__))

	DEBUG = False # debugger and helpful for auto reload when changes are made to the code

	SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "project/sample.db") # sqlite db location
	# SQLALCHEMY_DATABASE_URI = "sqlite:///sample.db" # sqlite db location
	SQLALCHEMY_TRACK_MODIFICATIONS = False # disabled for the time being

	SECRET_KEY = "\xc6\xbb\x98e3\xc7W\xe8\x81\xe3\xcfB\xb0*g^\xca\xfe\x19\x92\x8e\xd2#\x02" # used to create a cryptographic token to validate form

	RECAPTCHA_PUBLIC_KEY = '6LeYIbsSAAAAACRPIllxA7wvXjIE411PfdB2gt2J'
	RECAPTCHA_PRIVATE_KEY = '6LeYIbsSAAAAAJezaIq3Ft_hSTo0YtyeFG-JgRtu'
	# RECAPTCHA_API_SERVER = ? # recaptcha api server
	RECAPTCHA_DATA_ATTRS = {'theme': 'dark'}


class DevelopmentConfig(BaseConfig):
	''''''
	DEBUG = True


class TestingConfig(BaseConfig):
	''''''
	DEBUG = True
	TESTING = True
	WTF_CSRF_ENABLED = False

# class ProductionConfig(BaseConfig):
