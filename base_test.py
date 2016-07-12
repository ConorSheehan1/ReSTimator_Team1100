from app.app import restimatorApp
import unittest

class FlaskTest(unittest.TestCase):
	'''Test class'''

	# Home page testing

	def test_home(self):
		'''Test Flask set up correctly'''
		tester = restimatorApp.test_client(self) # create test client
		response = tester.get("/home", content_type="html/text")
		self.assertEqual(response.status_code, 200)

	def test_homepage_loads_correctly(self):
		'''Test Flask loads page correctly'''
		tester = restimatorApp.test_client(self)
		response = tester.get("/home", content_type="html/text")
		self.assertIn(b"ReSTimator - Home", response.data)

	# Sign up page testing

	def test_signup(self):
		'''Test Flask set up correctly'''
		tester = restimatorApp.test_client(self)
		response = tester.get("/sign_up", content_type="html/text")
		self.assertEqual(response.status_code, 200)

	def test_signuppage_loads_correctly(self):
		'''Test Flask loads page correctly'''
		tester = restimatorApp.test_client(self)
		response = tester.get("/sign_up", content_type="html/text")
		self.assertIn(b"ReSTimator - Sign Up", response.data)

	def test_signup_feature1(self):
		'''Test Sign up feature works correctly when given correct credentials'''
		pass
	# 	tester = restimatorApp.test_client(self)
	# 	response = tester.post("/sign_up", data=dict(username="x@ucd.ie", password="ucd", confirm="ucd", accept_terms=True), follow_redirects=True)
	# 	self.assertIn(b"Successfully Registered", response.data)

	def test_signup_feature2(self):
		'''Test Sign up feature works correctly when given incorrect credentials'''
		pass
	# 	tester = restimatorApp.test_client(self)
	# 	response = tester.post("/login", data=dict(username="x", password="ucd", confirm="udc", accept_terms=False))
	# 	self.assertIn(b"This field is required", response.data)

	# Login page testing

	def test_login(self):
		'''Test Flask set up correctly'''
		tester = restimatorApp.test_client(self)
		response = tester.get("/login", content_type="html/text")
		self.assertEqual(response.status_code, 200)

	def test_loginpage_loads_correctly(self):
		'''Test Flask loads page correctly'''
		tester = restimatorApp.test_client(self)
		response = tester.get("/login", content_type="html/text")
		self.assertIn(b"ReSTimator - Login", response.data)

	def test_login_feature1(self):
		'''Test Login feature works correctly when given correct credentials'''
		pass
	# 	tester = restimatorApp.test_client(self)
	# 	response = tester.post("/login", data=dict(username="x@ucd.ie", password="ucd", remember_me=False), follow_redirects=True)
	# 	self.assertIn(b"Login requested for Username=x@ucd.ie", response.data)

	def test_login_feature2(self):
		'''Test Login feature works correctly when given incorrect credentials'''
		pass
	# 	tester = restimatorApp.test_client(self)
	# 	response = tester.post("/login", data=dict(username="x", password="ucd", remember_me=False))
	# 	self.assertIn(b"This field is required", response.data)

	def test_login_feature3(self):
		'''Test Login feature requires user to login first'''
		pass
	# 	tester = restimatorApp.test_client(self)
	# 	response = tester.post("/", follow_redirects=True)
	# 	self.assertIn(b"Login first", response.data)

	# Analysis page testing

	def test_analysis(self):
		'''Test Flask set up correctly'''
		tester = restimatorApp.test_client(self) # create test client
		response = tester.get("/analysis", content_type="html/text")
		self.assertEqual(response.status_code, 200)

	def test_analysis_loads_correctly(self):
		'''Test Flask loads page correctly'''
		tester = restimatorApp.test_client(self)
		response = tester.get("/analysis", content_type="html/text")
		self.assertIn(b"ReSTimator - Analysis", response.data)

	# Data page testing

	def test_data(self):
		'''Test Flask set up correctly'''
		tester = restimatorApp.test_client(self) # create test client
		response = tester.get("/data", content_type="html/text")
		self.assertEqual(response.status_code, 200)

	def test_datapage_loads_correctly(self):
		'''Test Flask loads page correctly'''
		tester = restimatorApp.test_client(self)
		response = tester.get("/data", content_type="html/text")
		self.assertIn(b"ReSTimator - Data", response.data)

	# About page testing

	def test_about(self):
		'''Test Flask set up correctly'''
		tester = restimatorApp.test_client(self) # create test client
		response = tester.get("/about", content_type="html/text")
		self.assertEqual(response.status_code, 200)

	def test_aboutpage_loads_correctly(self):
		'''Test Flask loads page correctly'''
		tester = restimatorApp.test_client(self)
		response = tester.get("/about", content_type="html/text")
		self.assertIn(b"ReSTimator - About", response.data)

	# Contact page testing

	def test_contact(self):
		'''Test Flask set up correctly'''
		tester = restimatorApp.test_client(self) # create test client
		response = tester.get("/contact", content_type="html/text")
		self.assertEqual(response.status_code, 200)

	def test_contactpage_loads_correctly(self):
		'''Test Flask loads page correctly'''
		tester = restimatorApp.test_client(self)
		response = tester.get("/contact", content_type="html/text")
		self.assertIn(b"ReSTimator - Contact", response.data)


if __name__ == "__main__":
	unittest.main()