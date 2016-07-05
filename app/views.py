from flask import render_template, flash, redirect, url_for, request
# from flask_login import login_required, current_user
from app import restimatorApp, db, tables
from .login import LoginForm
from .sign_up import RegistrationForm
from .analysis import AnalysisForm

@restimatorApp.route("/")
@restimatorApp.route("/home", methods=["GET", "POST"])
def home():
    '''home view''' 
    random = tables.Users.query.all()
    return render_template("home.html", random=random) # function takes a template filename and a variable list of template args and returns the rendered template (invokes Jinja2 templating engine)

@restimatorApp.route('/login', methods=["GET", "POST"]) # view function accepts both GET and POST requests
def login():
	'''form view'''
	form = LoginForm() # create instance of LoginForm
	if form.validate_on_submit(): # validate_on_submit method processes form on form submission request. Returns true if all validators attached to fields pass (need more validators in form)
		flash("Login requested for Username=%s, remember_me=%s" % (form.username.data, str(form.remember_me.data))) # returns a message on next page to user
		return redirect("/home") # redirect tells the client web browser to navigate to a different page
	return render_template("login.html", title="Sign In", form=form) # pass LoginForm object to template

@restimatorApp.route("/sign_up", methods=["GET", "POST"])
def sign_up():
    '''Sign up view'''
    form = RegistrationForm() # create instance of RegistrationForm
    if request.method == 'POST' and form.validate():
        user = tables.Users(form.username.data, form.password.data) 
        db.session.add(user)
        db.session.commit()
        flash("Successfully Registered")
        return redirect("/home") # redirect(url_for("/home"))
    return render_template("sign_up.html", form=form)

@restimatorApp.route("/analysis", methods=["GET", "POST"])
def analysis():
    '''about view'''
    form = AnalysisForm()
    return render_template("analysis.html", form=form)

@restimatorApp.route("/about")
def about():
    '''about view'''
    return render_template("about.html")

@restimatorApp.route("/data")
def data():
    '''data view'''
    return render_template("data.html")

@restimatorApp.route("/contact")
def contact():
    '''data view'''
    return render_template("contact.html")