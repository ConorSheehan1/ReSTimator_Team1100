import os 


class BaseConfig():
	''''''
	basedir = os.path.abspath(os.path.dirname(__file__))

	DEBUG = False # debugger and helpful for auto reload when changes are made to the code

	SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "project/restimator.db") # sqlite db location
	SQLALCHEMY_TRACK_MODIFICATIONS = False # disabled for the time being

	SECRET_KEY = "\xc6\xbb\x98e3\xc7W\xe8\x81\xe3\xcfB\xb0*g^\xca\xfe\x19\x92\x8e\xd2#\x02" # used to create a cryptographic token to validate form

	RECAPTCHA_PUBLIC_KEY = '6LdXiycTAAAAACbhoxsHDKqVD57LW51bmvssm2CZ'
	RECAPTCHA_PRIVATE_KEY = '6LdXiycTAAAAAHka12ZKw6TPTeE4edUZJ2VkQHvB'
	RECAPTCHA_DATA_ATTRS = {'theme': 'dark'}

	# main config
	SECURITY_PASSWORD_SALT = 'salty_salt'
	BCRYPT_LOG_ROUNDS = 13
	WTF_CSRF_ENABLED = True
	DEBUG_TB_ENABLED = False
	DEBUG_TB_INTERCEPT_REDIRECTS = False

	# mail settings
	MAIL_DEFAULT_SENDER = 'ucd.restimator@gmail.com'
	MAIL_SERVER = 'smtp.googlemail.com'
	MAIL_PORT = 465
	MAIL_USE_TLS = False
	MAIL_USE_SSL = True

	# gmail authentication
	MAIL_USERNAME = 'ucd.restimator'
	MAIL_PASSWORD = 'give_it_a_rest'
	
	# path to the upload directory
	UPLOAD_FOLDER = './data/log_data'


class DevelopmentConfig(BaseConfig):
	''''''
	DEBUG = True
	ACCEPTABLE_SUFFIX = ".ie"


class TestingConfig(BaseConfig):
	''''''
	DEBUG = True
	TESTING = True
	WTF_CSRF_ENABLED = False
	ACCEPTABLE_SUFFIX = ".ie"


class ProductionConfig(BaseConfig):
	''''''
	DEBUG = False
	ACCEPTABLE_SUFFIX = "@ucd.ie"
