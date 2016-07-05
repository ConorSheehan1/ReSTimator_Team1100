from app import db

# Declarative Base - http://pythoncentral.io/introductory-tutorial-python-sqlalchemy/
'''The baseclass for all your models is called db.Model. 
It’s stored on the SQLAlchemy instance you have to create. 

Some parts that are required in SQLAlchemy are optional in Flask-SQLAlchemy i.e.
Table name is automatically set for you unless overridden (derived from the class name converted to lowercase and with “CamelCase” converted to “camel_case”)
Column to define a column (named after variable name)
Types: Integer / String (size) / Text -	longer unicode text / DateTime - expressed as Python datetime object / Float / Boolean / PickleType / LargeBinary	
Primary keys are marked with primary_key=True
'''

class Users(db.Model):
	''''''
	username = db.Column(db.String(80), primary_key=True) # Column to define a column
	password = db.Column(db.String(120))

	def __init__(self, username, password):
		''''''
		self.username = username
		self.password = password

	def __repr__(self):
		''''''
		return "<User: %s>" % self.username

class Results(db.Model):
	''''''
	day = db.Column(db.String(3), primary_key=True)
	time = db.Column(db.String(20), primary_key=True)
	module = db.Column(db.String(10), primary_key=True)
	estimate = db.Column(db.Integer)

	def __init__(self, day, time, module, estimate):
		''''''
		self.day = day
		self.time = time
		self.module = module
		self.estimate = estimate

	def __repr__(self):
		''''''
		return "<Day: %s, Time: %s, Module Code: %s, Est.: %d>" % (self.day, self.time, self.module, self.estimate)

class Location(db.Model):
	''''''
	campus = db.Column(db.String(45), unique=True)
	building = db.Column(db.String(45), primary_key=True)
	room = db.Column(db.String(10), primary_key=True)
	capacity = db.Column(db.Integer)
	occupy = db.relationship("Occupy", backref="location", lazy="dynamic") 

	def __init__(self, campus, building, room, capacity):
		''''''
		self.campus = campus
		self.building = building
		self.room = room
		self.capacity = capacity

	def __repr__(self):
		''''''
		return "<Campus: %s, Building: %s, Room: %s, Capacity: %d" % (self.campus, self.building, self.room, self.capacity)

class Module(db.Model):
	''''''
	code = db.Column(db.String(10), primary_key=True)
	reg_students = db.Column(db.Integer)
	occupy = db.relationship("Occupy", backref="module", lazy="dynamic") # not a column / backref adds a virtual column

	def __init__(self, code, reg_students):
		''''''
		self.code = code
		self.reg_students = reg_students

	def __repr__(self):
		''''''
		return "<Module Code: %s, Registered Students: %d" % (self.code, self.reg_students)

class Occupy(db.Model):
	day = db.Column(db.String(3))
	time = db.Column(db.String(20), primary_key=True)
	date = db.Column(db.String(20), primary_key=True)
	ground_truth = db.Column(db.Integer)
	auth = db.Column(db.Integer)
	assoc = db.Column(db.Integer)
	module_code = db.Column(db.String(10), db.ForeignKey("module.code"), primary_key=True)
	room_id = db.Column(db.String(10), db.ForeignKey("location.room"), primary_key=True)

	def __init__(self, day, time, date, module, room, ground_truth, auth, assoc):
		''''''
		self.day = day
		self.time = time
		self.date = date
		self.ground_truth = ground_truth
		self.auth = auth
		self.assoc = assoc
		self.module_code = module_code
		self.room_id = room_id

	def __repr__(self):
		return "<Day: %s, Time: %s, Date: %s, Module Code: %s, Room: %s, Ground Truth: %d, Authenticated: %d, Associated: %d" % (self.day, self.time, self.date, self.module_code, self.room_id, self.ground_truth, self.auth, self.assoc)
