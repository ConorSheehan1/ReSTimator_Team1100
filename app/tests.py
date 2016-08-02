import unittest
from flask.ext.testing import TestCase
from project import restimatorApp, db
from project.models import *


class BaseTest(TestCase):
	''''''

	def create_app(self):
		''''''
		restimatorApp.config.from_object("config.TestingConfig")
		return restimatorApp

	def set_db_up(self):
		''''''
		db.create_all()
		db.seesion.add(Users(username="admin@ucd.ie", password="admin")) # for testing  login functionality
		db.session.commit()

	def tear_db_down(self):
		''''''
		db.session.remove()
		db.drop_all()


class FlaskTest(BaseTest):
	'''Test class'''

	# Home page testing

	# def test_home(self):
	# 	'''Test Flask set up correctly'''
	# 	response = self.client.get("/home", content_type="html/text")
	# 	self.assertEqual(response.status_code, 200)

	# def test_homepage_loads_correctly(self):
	# 	'''Test Flask loads page correctly'''
	# 	response = self.client.get("/home", content_type="html/text")
	# 	self.assertIn(b"ReSTimator - Home", response.data)

	# Sign up page testing

	def test_signup(self):
		'''Test Flask set up correctly'''
		response = self.client.get("/sign_up", content_type="html/text")
		self.assertEqual(response.status_code, 200)

	def test_signuppage_loads_correctly(self):
		'''Test Flask loads page correctly'''
		response = self.client.get("/sign_up", content_type="html/text")
		self.assertIn(b"ReSTimator - Sign Up", response.data)

	def test_signup_feature1(self):
		'''Test Sign up feature works correctly when given correct credentials'''
		pass
	# 	response = self.client.post("/sign_up", data=dict(username="x@ucd.ie", password="ucd", confirm="ucd", accept_terms=True), follow_redirects=True)
	# 	self.assertIn(b"Successfully Registered", response.data)

	def test_signup_feature2(self):
		'''Test Sign up feature works correctly when given incorrect credentials'''
		pass
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

	def test_login_feature1(self):
		'''Test Login feature works correctly when given correct credentials'''
		response = self.client.post("/login", data=dict(username="admin@ucd.ie", password="admin"), follow_redirects=True) 
		self.assertIn(b"Login requested for Username=admin@ucd.ie", response.data)

	def test_login_feature2(self):
		'''Test Login feature works correctly when given incorrect credentials'''
		response = self.client.post("/login", data=dict(username="x@ucd.ie", password=None), follow_redirects=True) 
		self.assertIn(b"This field is required", response.data)
		response = self.client.post("/login", data=dict(username="admin", password="admin"), follow_redirects=True) 
		self.assertIn(b"Invalid email address", response.data)

	def test_login_feature3(self):
		'''Test Login feature requires user to login first'''
		response = self.client.post("/home", follow_redirects=True)
		self.assertIn(b"Please log in to access this page.", response.data)

	# Analysis page testing

	# def test_analysis(self):
	# 	'''Test Flask set up correctly'''
	# 	response = self.client.get("/analysis", content_type="html/text")
	# 	self.assertEqual(response.status_code, 200)

	# def test_analysis_loads_correctly(self):
	# 	'''Test Flask loads page correctly'''
	# 	response = self.client.get("/analysis", content_type="html/text")
	# 	self.assertIn(b"ReSTimator - Analysis", response.data)

	# Data page testing

	# def test_data(self):
	# 	'''Test Flask set up correctly'''
	# 	response = self.client.get("/data", content_type="html/text")
	# 	self.assertEqual(response.status_code, 200)

	# def test_datapage_loads_correctly(self):
	# 	'''Test Flask loads page correctly'''
	# 	response = self.client.get("/data", content_type="html/text")
	# 	self.assertIn(b"ReSTimator - Data", response.data)

	# About page testing

	def test_about(self):
		'''Test Flask set up correctly'''
		response = self.client.get("/about", content_type="html/text")
		self.assertEqual(response.status_code, 200)

	def test_aboutpage_loads_correctly(self):
		'''Test Flask loads page correctly'''
		response = self.client.get("/about", content_type="html/text")
		self.assertIn(b"ReSTimator - About", response.data)

	# Contact page testing

	def test_contact(self):
		'''Test Flask set up correctly'''
		response = self.client.get("/contact", content_type="html/text")
		self.assertEqual(response.status_code, 200)

	def test_contactpage_loads_correctly(self):
		'''Test Flask loads page correctly'''
		response = self.client.get("/contact", content_type="html/text")
		self.assertIn(b"ReSTimator - Contact", response.data)


if __name__ == "__main__":
	unittest.main()