from flask import render_template, flash, redirect, url_for, request
# from flask_login import login_required, current_user
from .app import restimatorApp, db
from .login import LoginForm
from .sign_up import RegistrationForm
from .analysis import AnalysisForm
from .tables import * # import database objects

@restimatorApp.route("/")
@restimatorApp.route("/home", methods=["GET", "POST"])
def home():
    '''home view'''
    pg_name = "Home" 
    random = db.session.query(Users).all()
    return render_template("home.html", pg_name=pg_name, random=random) # function takes a template filename and a variable list of template args and returns the rendered template (invokes Jinja2 templating engine)

@restimatorApp.route('/login', methods=["GET", "POST"]) # view function accepts both GET and POST requests
def login():
    '''form view'''
    pg_name = "Login" 
    form = LoginForm() # create instance of LoginForm
    if request.method == "POST" and form.validate_on_submit(): # validate_on_submit method processes form on form submission request. Returns true if all validators attached to fields pass (need more validators in form)
    	flash("Login requested for Username=%s" % (form.username.data)) # returns a message on next page to user
    	return redirect("/home") # redirect tells the client web browser to navigate to a different page
    return render_template("login.html", pg_name=pg_name, title="Sign In", form=form) # pass LoginForm object to template

@restimatorApp.route("/sign_up", methods=["GET", "POST"])
def sign_up():
    '''Sign up view'''
    pg_name = "Sign Up" 
    form = RegistrationForm() # create instance of RegistrationForm
    if request.method == "POST" and form.validate():
        user = Users(form.username.data, form.password.data) 
        db.session.add(user)
        db.session.commit()
        flash("Successfully Registered")
        return redirect("/home") # redirect(url_for("/home"))
    return render_template("sign_up.html", pg_name=pg_name, form=form)

@restimatorApp.route("/analysis", methods=["GET", "POST"])
def analysis():
    '''analysis view'''
    pg_name = "Analysis" 
    form = AnalysisForm()
    query = ""
    if request.method == "POST" and form.validate_on_submit():
        query = Results.query.filter_by(day=form.day.data, time=form.time.data, module=form.module.data).all()
    return render_template("analysis.html", pg_name=pg_name, form=form, query=query)

@restimatorApp.route("/about")
def about():
    '''about view'''
    pg_name = "About" 
    return render_template("about.html", pg_name=pg_name)

@restimatorApp.route("/data")
def data():
    '''data view'''
    pg_name = "Data" 
    return render_template("data.html", pg_name=pg_name)

@restimatorApp.route("/contact")
def contact():
    '''contact view'''
    pg_name = "Contact" 
    return render_template("contact.html", pg_name=pg_name)

# @csrf.error_handler
# def csrf_error(reason):
#     return render_template('csrf_error.html', reason=reason), 400


