import unittest
from flask.ext.testing import TestCase
from project import app, db
from project.models import *


class BaseTest(TestCase):
	''''''

	def create_app(self):
		''''''
		app.config.from_object("config.TestingConfig")
		return app

	def set_db_up(self):
		''''''
		try:
			db.create_all()
			db.session.add(Users(username="admin@ucd.ie", password="admin")) # for testing  login functionality
			db.session.commit()
		except:
			print("values already in db")

	def tear_db_down(self):
		''''''
		db.session.remove()
		db.drop_all()


class FlaskTest(BaseTest):
	'''Test class'''

	# Home page testing
	def test_home(self):
		'''Test Flask set up correctly'''
		response = self.client.get("/home", content_type="html/text")
		self.assertEqual(response.status_code, 200)

	def test_homepage_loads_correctly(self):
		'''Test Flask loads page correctly'''
		response = self.client.get("/home", content_type="html/text")
		self.assertIn(b"ReSTimator - Home", response.data)

	# Sign up page testing

	def test_signup(self):
		'''Test Flask set up correctly'''
		response = self.client.get("/sign_up", content_type="html/text")
		self.assertEqual(response.status_code, 200)

	def test_signuppage_loads_correctly(self):
		'''Test Flask loads page correctly'''
		response = self.client.get("/sign_up", content_type="html/text")
		self.assertIn(b"ReSTimator - Sign Up", response.data)

	# def test_signup_feature1(self):
	# 	'''Test Sign up feature works correctly when given correct credentials'''
	# 	pass
	# # 	response = self.client.post("/sign_up", data=dict(username="x@ucd.ie", password="ucd", confirm="ucd", accept_terms=True), follow_redirects=True)
	# # 	self.assertIn(b"Successfully Registered", response.data)
    #
	# def test_signup_feature2(self):
	# 	'''Test Sign up feature works correctly when given incorrect credentials'''
	# 	pass
	# 	response = self.client.post("/login", data=dict(username="x", password="ucd", confirm="udc", accept_terms=False))
	# 	self.assertIn(b"This field is required", response.data)

	# Login page testing

	def test_login(self):
		'''Test Flask set up correctly'''
		response = self.client.get("/login", content_type="html/text")
		self.assertEqual(response.status_code, 200)

	def test_loginpage_loads_correctly(self):
		'''Test Flask loads page correctly'''
		response = self.client.get("/login", content_type="html/text")
		self.assertIn(b"ReSTimator - Login", response.data)

	# def test_login_feature1(self):
	# 	'''Test Login redirects to home when given correct credentials'''
	# 	response = self.client.post("/login", data=dict(username="admin@ucd.ie", password="admin"), follow_redirects=True)
	# 	self.assertIn(b"ReSTimator - Home", response.data)
    #
	# def test_login_feature2(self):
	# 	'''Test Login feature works correctly when given incorrect credentials'''
	# 	response = self.client.post("/login", data=dict(username="x@ucd.ie", password=None), follow_redirects=True)
	# 	self.assertIn(b"This field is required", response.data)
	# 	response = self.client.post("/login", data=dict(username="admin", password="admin"), follow_redirects=True)
	# 	self.assertIn(b"Invalid email address", response.data)
    #
	# def test_login_feature3(self):
	# 	'''Test Login feature requires user to login first'''
	# 	response = self.client.post("/home", follow_redirects=True)
	# 	self.assertIn(b"Please log in to access this page.", response.data)

	# Analysis page testing

	# def test_analysis(self):
	# 	'''Test Flask set up correctly'''
	# 	response = self.client.get("/analysis", content_type="html/text")
	# 	self.assertEqual(response.status_code, 200)

	# def test_analysis_loads_correctly(self):
	# 	'''Test Flask loads page correctly'''
	# 	response = self.client.get("/analysis", content_type="html/text")
	# 	self.assertIn(b"ReSTimator - Analysis", response.data)

	# test db
	def test_num_rows_occupy(self):
		'''
		Test that the correct number of rows are inserted in the db upon start
		'''
		rows = db.session.query(Occupy).count()
		assert rows >= 12603

	def test_num_rows_location(self):
		rows = db.session.query(Location).count()
		assert rows >= 3

	def test_num_rows_module(self):
		rows = db.session.query(Module).count()
		assert rows >= 40

	def test_time_format(self):
		'''
		Hours should be between 00 and 24
		Minutes should be between 0 and 59
		'''
		times = db.session.query(Occupy.time).all()
		for tup in times:
			try:
				hours = int(tup[0].split(":")[0])
				minutes = int(tup[0].split(":")[1])
			except:
				print("Time format changed")
				assert False
			# if hours isn't between 0 and 23
			if not(0 <= hours <= 23):
				assert False

			# if minutes isn't between 0 and 59
			if not(0 <= minutes <= 59):
				assert False

		# if all other cases don't fail, test has passed
		assert True

	def test_date_format(self):
		'''
		year should always be positive
		month should be between 1 and 12
		day should be between 1 and 31
		'''
		dates = db.session.query(Occupy.date).all()
		for tup in dates:
			try:
				year = int(tup[0].split("-")[0])
				month = int(tup[0].split("-")[1])
				day = int(tup[0].split("-")[2])
			except:
				print("date format has changed")
				assert False
			if year < 0:
				assert False

			# if month isn't between 1 and 12
			if not(1 <= month <= 12):
				assert False

			# if day isn't between 1 and 31
			if not(1 <= day <= 31):
				assert False
		# if all other cases don't fail, test has passed
		assert True

	def test_occupany_format(self):
		'''
		Occupancy should always be a float between 0 and 1
		'''
		occupancy = db.session.query(Occupy.occupancy).all()
		for tup in occupancy:
			# if tuple has a value and it's not between 0 and 1
			if tup[0] is not None and (not(0.0 <= tup[0] <= 1.0)):
				assert False
		assert True

	def test_client_counts(self):
		'''
		client counts should always be positive integers
		'''
		associated = db.session.query(Occupy.associated_client_count).all()
		authenticated = db.session.query(Occupy.authenticated_client_count).all()
		# if any value in associated or authenticated is negative, fail test
		for tup in associated:
			if tup[0] is not None and tup[0] < 0:
				assert False
		for tup in authenticated:
			if tup[0] is not None and tup[0] < 0:
				assert False
		assert True

	def test_room_format(self):
		'''
		room codes should always begin with a letter and end with a number
		'''
		rooms = db.session.query(Occupy.room).all()
		for tup in rooms:
			room = tup[0]
			try:
				letter = room.split("-")[0]
				number = room.split("-")[1]
			except:
				print("room format changed")
				assert False

			if not(letter.isalpha() and number.isnumeric()):
				assert False
		assert True

	def test_capacity_format(self):
		'''
		capacity should always be positive integers
		'''
		capacity = db.session.query(Location.capacity).all()
		for tup in capacity:
			if tup[0] < 0:
				assert False
		assert True

	def test_reg_students_format(self):
		'''
		reg_students should always be positive integers
		'''
		reg = db.session.query(Module.reg_students).all()
		for tup in reg:
			if tup[0] < 0:
				assert False
		assert True

	def test_module_code_format(self):
		'''
		module code should always start with a letter and end with a digit,
		even ones split into p1, p2 and joint modules
		'''
		modules = db.session.query(Module.module_code).all()
		for tup in modules:
			if not(tup[0][0].isalpha() and tup[0][-1].isnumeric()):
				assert False
		assert True

if __name__ == "__main__":
	unittest.main()
