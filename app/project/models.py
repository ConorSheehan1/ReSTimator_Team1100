from project import db # import database object
from werkzeug.security import generate_password_hash, check_password_hash # http://flask.pocoo.org/snippets/54/
# import datetime

'''The baseclass for all your models is called db.Model. 
It's stored on the SQLAlchemy instance you have to create. 

Some parts that are required in SQLAlchemy are optional in Flask-SQLAlchemy i.e.
Table name is automatically set for you unless overridden (derived from the class name converted to lowercase and with "CamelCase" converted to "camel_case")
Column to define a column (named after variable name)
Types: Integer / String (size) / Text -	longer unicode text / DateTime - expressed as Python datetime object / Float / Boolean / PickleType / LargeBinary	
Primary keys are marked with primary_key=True
'''


class Users(db.Model):
	'''Database object - application user login details'''
	# __tablename__ = "users" # can specify table name here if needed
	username = db.Column(db.String(80), primary_key=True, nullable=False) # Column to define a column
	password = db.Column(db.String(120), nullable=False)
	role = db.Column(db.String(8), nullable=False)
	# registered_on = db.Column(db.DateTime, nullable=False)
	# admin = db.Column(db.Boolean, nullable=False, default=False)
	# confirmed = db.Column(db.Boolean, nullable=False, default=False)
	# confirmed_on = db.Column(db.DateTime, nullable=True)

	def __init__(self, username, password, role='normal'):
	# def __init__(self, username, password, confirmed, paid=False, admin=False, confirmed_on=None):
		'''instance attributes'''
		self.username = username
		self.password = self.set_password(password)
		self.role = role
        # self.registered_on = datetime.datetime.now()
        # self.admin = admin
        # self.confirmed = confirmed
        # self.confirmed_on = confirmed_on


	def __repr__(self):
		'''object representation'''
		return "{} - {}".format(self.username, self.password)

	def set_password(self, password):
		''''''
		self.pw_hash = generate_password_hash(password)
		return self.pw_hash

	def check_password(self, password):
		''''''
		return check_password_hash(self.password, password)

	def is_authenticated(self):
		'''Returns True if the user is authenticated i.e. user provided valid credentials'''
		return True

	def is_active(self):
		'''Returns True if this is an active user 

		i.e. authenticated and user account is activated.
		Inactive accounts may not log in 
		'''
		return True

	def is_anonymous(self):
		'''Returns False if this is an anonymous user'''
		return False

	def get_id(self):
		'''Returns a unicode uniquely identifing the user'''
		return str(self.username)


class Results(db.Model):
	'''Database object'''
	model_type = db.Column(db.String(10), primary_key=True)
	model = db.Column(db.PickleType)
	accuracy = db.Column(db.String(200))

	def __init__(self, model_type, model, accuracy):
		'''instance attributes'''
		self.model_type = model_type
		self.model = model
		self.accuracy = accuracy


class Location(db.Model):
	'''Database object'''
	campus = db.Column(db.String(45), primary_key=True)
	building = db.Column(db.String(45), primary_key=True)
	room = db.Column(db.String(10), primary_key=True)
	capacity = db.Column(db.Integer)
	occupy = db.relationship("Occupy", backref="location", lazy="dynamic") 

	def __init__(self, campus, building, room, capacity):
		'''instance attributes'''
		self.campus = campus
		self.building = building
		self.room = room
		self.capacity = capacity

	def __repr__(self):
		'''object representation'''
		return "{} - {} - {} - {}".format(self.campus, self.building, self.room, self.capacity)


class Module(db.Model):
	'''Database object'''
	module_code = db.Column(db.String(10), primary_key=True)
	reg_students = db.Column(db.Integer)
	occupy = db.relationship("Occupy", backref="module", lazy="dynamic") # not a column / backref adds a virtual column

	def __init__(self, module_code, reg_students):
		'''instance attributes'''
		self.module_code = module_code
		self.reg_students = reg_students

	def __repr__(self):
		'''object representation'''
		return "{} - {}".format(self.module_code, self.reg_students)


class Occupy(db.Model):
	'''Database object'''
	room = db.Column(db.String(10), db.ForeignKey("location.room"), primary_key=True)
	date = db.Column(db.String(10), primary_key=True)
	time = db.Column(db.String(20), primary_key=True)
	occupancy = db.Column(db.Integer)
	module_code = db.Column(db.String(10), db.ForeignKey("module.module_code"))
	associated_client_count = db.Column(db.Integer)
	authenticated_client_count = db.Column(db.Integer)
	
	def __init__(self, room, date, time, module_code, occupancy, associated_client_count, authenticated_client_count):
		'''instance attributes'''
		self.room = room
		self.date = date
		self.time = time
		self.occupancy = occupancy
		self.module_code = module_code
		self.associated_client_count = associated_client_count
		self.authenticated_client_count = authenticated_client_count
		
	def __repr__(self):
		'''object representation'''
		return "{} - {} - {} - {} - {} - {} - {}".format(self.room, self.date, self.time, self.occupancy, self.module_code, self.associated_client_count, self.authenticated_client_count)
