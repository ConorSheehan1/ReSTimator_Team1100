from flask import Flask, render_template, flash, redirect, url_for, request, session, Blueprint
from functools import wraps 
from .login_form import LoginForm

users_blueprint = Blueprint("users", __name__, template_folder="templates")

def login_required(test):
	'''If user tries to send GET request and they are not logged in i.e. no logged_in key, then this function will redirect user back to login page'''
	@wraps(test)
	def wrap(*args, **kwargs):
		if "logged_in" in session:
			return test(*args, **kwargs)
		else:
			flash("Required to log in to view page")
		return redirect(url_for("users.login"))
	return wrap

# route for handling the login page logic
@users_blueprint.route("/login", methods=["GET", "POST"]) # view function accepts both GET and POST requests
def login():
	'''form view'''
	pg_name = "Login" 
	form = LoginForm() # create instance of LoginForm
	if request.method == "POST" and form.validate_on_submit():
		session["logged_in"] = True # if user credentials are correct, set to true
		flash("Login requested for Username=%s" % (form.username.data)) # returns a message on next page to user
		return redirect("/home") # redirect tells the client web browser to navigate to a different page
	return render_template("login.html", pg_name=pg_name, title="Sign In", form=form) # pass LoginForm object to template

@users_blueprint.route("/logout")
@login_required
def logout():
    session.pop("logged_in", None) # When a GET response set to this route, True is popped and replaced with none, then user is redirected to login page
    flash("User logged out")
    return redirect(url_for("users.login"))