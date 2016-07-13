# from app import db # import database object

# # Declarative Base - http://pythoncentral.io/introductory-tutorial-python-sqlalchemy/
# '''The baseclass for all your models is called db.Model. 
# It’s stored on the SQLAlchemy instance you have to create. 

# Some parts that are required in SQLAlchemy are optional in Flask-SQLAlchemy i.e.
# Table name is automatically set for you unless overridden (derived from the class name converted to lowercase and with “CamelCase” converted to “camel_case”)
# Column to define a column (named after variable name)
# Types: Integer / String (size) / Text -	longer unicode text / DateTime - expressed as Python datetime object / Float / Boolean / PickleType / LargeBinary	
# Primary keys are marked with primary_key=True
# '''

# class Users(db.Model):
# 	'''Database object'''
# 	# class variables
# 	# __tablename__ = "users" # can specify table name here if needed
# 	username = db.Column(db.String(80), primary_key=True, nullable=False) # Column to define a column
# 	password = db.Column(db.String(120), nullable=False)

# 	def __init__(self, username, password):
# 		'''instance attributes'''
# 		self.username = username
# 		self.password = password

# 	def __repr__(self):
# 		'''object representation'''
# 		return "{} - {}".format(self.username, self.password)

# class Results(db.Model):
# 	'''Database object'''
# 	day = db.Column(db.String(3), primary_key=True)
# 	time = db.Column(db.String(20), primary_key=True)
# 	module = db.Column(db.String(10), primary_key=True)
# 	estimate = db.Column(db.Integer)

# 	def __init__(self, day, time, module, estimate):
# 		'''instance attributes'''
# 		self.day = day
# 		self.time = time
# 		self.module = module
# 		self.estimate = estimate

# 	def __repr__(self):
# 		'''object representation'''
# 		return "{} - {}".format(self.day, self.time, self.module, self.estimate)

# class Location(db.Model):
# 	'''Database object'''
# 	campus = db.Column(db.String(45), unique=True)
# 	building = db.Column(db.String(45), primary_key=True)
# 	room = db.Column(db.String(10), primary_key=True)
# 	capacity = db.Column(db.Integer)
# 	occupy = db.relationship("Occupy", backref="location", lazy="dynamic") 

# 	def __init__(self, campus, building, room, capacity):
# 		'''instance attributes'''
# 		self.campus = campus
# 		self.building = building
# 		self.room = room
# 		self.capacity = capacity

# 	def __repr__(self):
# 		'''object representation'''
# 		return "{} - {}".format(self.campus, self.building, self.room, self.capacity)

# class Module(db.Model):
# 	'''Database object'''
# 	code = db.Column(db.String(10), primary_key=True)
# 	reg_students = db.Column(db.Integer)
# 	occupy = db.relationship("Occupy", backref="module", lazy="dynamic") # not a column / backref adds a virtual column

# 	def __init__(self, code, reg_students):
# 		'''instance attributes'''
# 		self.code = code
# 		self.reg_students = reg_students

# 	def __repr__(self):
# 		'''object representation'''
# 		return "{} - {}".format(self.code, self.reg_students)

# class Occupy(db.Model):
# 	'''Database object'''
# 	day = db.Column(db.String(3))
# 	time = db.Column(db.String(20), primary_key=True)
# 	date = db.Column(db.String(20), primary_key=True)
# 	ground_truth = db.Column(db.Integer)
# 	auth = db.Column(db.Integer)
# 	assoc = db.Column(db.Integer)
# 	module_code = db.Column(db.String(10), db.ForeignKey("module.code"), primary_key=True)
# 	room_id = db.Column(db.String(10), db.ForeignKey("location.room"), primary_key=True)

# 	def __init__(self, day, time, date, module, room, ground_truth, auth, assoc):
# 		'''instance attributes'''
# 		self.day = day
# 		self.time = time
# 		self.date = date
# 		self.ground_truth = ground_truth
# 		self.auth = auth
# 		self.assoc = assoc
# 		self.module_code = module_code
# 		self.room_id = room_id

# 	def __repr__(self):
# 		'''object representation'''
# 		return "{} - {}".format(self.day, self.time, self.date, self.module_code, self.room_id, self.ground_truth, self.auth, self.assoc)
