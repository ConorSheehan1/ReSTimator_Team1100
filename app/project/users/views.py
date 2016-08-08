from flask import Flask, render_template, flash, redirect, url_for, request, Blueprint
from .forms import LoginForm, SignUpForm
from flask.ext.login import login_user, login_required, logout_user
from project.models import Users
from project import db
import sqlalchemy

users_blueprint = Blueprint("users", __name__, template_folder="templates")


@users_blueprint.route("/login", methods=["GET", "POST"]) # route for handling the login page logic. view function accepts both GET and POST requests
def login():
    '''form view'''
    pg_name = "Login"
    error = None
    form = LoginForm(request.form) # create instance of LoginForm request.form
    if request.method == "POST" and form.validate_on_submit():
        user = Users.query.filter_by(username=request.form["username"]).first()
        if user is not None and user.check_password(form.password.data): 
            login_user(user) # function manages session cookie. User model needs to be updated to allow user to be considered active
            flash("User %s logged in successfully" % (form.username.data)) # returns a message on next page to user
            return redirect(url_for("main.home")) # redirect tells the client web browser to navigate to a different page
        else:
            error = "Invalid user credentials. Please try again."
    return render_template("login.html", pg_name=pg_name, title="Sign In", form=form, error=error) # pass LoginForm object to template


@users_blueprint.route("/logout")
@login_required
def logout():
    ''''''
    logout_user() # logs out user and cleans out session cookie
    flash("User logged out")
    return redirect(url_for("users.login"))


@users_blueprint.route("/sign_up", methods=["GET", "POST"])
def sign_up():
    '''Sign up view'''
    pg_name = "Sign Up" 
    form = SignUpForm() # create instance of RegistrationForm
    # flash("Please Register")
    if request.method == "POST" and form.validate_on_submit():
        user = Users(username=form.username.data, password=form.password.data) 
        # user = Users(username=form.username.data, password=form.password.data, confirmed=False) 
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash("Successfully Registered")
        return redirect(url_for("main.home"))
    return render_template("sign_up.html", pg_name=pg_name, form=form)
