# # from flask import Flask, render_template, flash, redirect, url_for, request, session
# from functools import wraps  
# # from flask_sqlalchemy import SQLAlchemy
# # from flask_wtf.csrf import CsrfProtect

# ###CONFIGURATION###

# # restimatorApp = Flask(__name__) # application object
# # CsrfProtect(restimatorApp) # enables CSRF protection for all view handlers
# # restimatorApp.config.from_object("config.DevelopmentConfig") # read and use config file
# # db = SQLAlchemy(restimatorApp) # sqlalchemy database object

# ###VIEWS: handlers that respond to requests from browsers. Flask handlers are written as functions (each view function is mapped to one or more request URLs)###
# from sign_up import RegistrationForm
# from analysis import AnalysisForm
# # from models import * 
# # from project.users.views import users_blueprint

# # # # Register blueprint
# # restimatorApp.register_blueprint(users_blueprint)

# def login_required(test):
#     '''If user tries to send GET request and they are not logged in i.e. no logged_in key, then this function will redirect user back to login page'''
#     @wraps(test)
#     def wrap(*args, **kwargs):
#         if 'logged_in' in session:
#             return test(*args, **kwargs)
#         else:
#             flash("Required to log in to view page")
#             return redirect(url_for("users.login"))
#     return wrap

# @restimatorApp.route("/")
# @restimatorApp.route("/home", methods=["GET", "POST"])
# @login_required
# def home():
#     '''home view'''
#     pg_name = "Home" 
#     random = db.session.query(Users).all()
#     return render_template("home.html", pg_name=pg_name, random=random) # function takes a template filename and a variable list of template args and returns the rendered template (invokes Jinja2 templating engine)

# @restimatorApp.route("/sign_up", methods=["GET", "POST"])
# def sign_up():
#     '''Sign up view'''
#     pg_name = "Sign Up" 
#     form = RegistrationForm() # create instance of RegistrationForm
#     if request.method == "POST" and form.validate():
#         user = Users(form.username.data, form.password.data) 
#         db.session.add(user)
#         db.session.commit()
#         flash("Successfully Registered")
#         return redirect("/home") # redirect(url_for("/home"))
#     return render_template("sign_up.html", pg_name=pg_name, form=form)

# @restimatorApp.route("/analysis", methods=["GET", "POST"])
# @login_required
# def analysis():
#     '''analysis view'''
#     pg_name = "Analysis" 
#     form = AnalysisForm()
#     query = ""
#     if request.method == "POST" and form.validate_on_submit():
#         query = Results.query.filter_by(day=form.day.data, time=form.time.data, module=form.module.data).all()
#     return render_template("analysis.html", pg_name=pg_name, form=form, query=query)

# @restimatorApp.route("/about")
# def about():
#     '''about view'''
#     pg_name = "About" 
#     return render_template("about.html", pg_name=pg_name)

# @restimatorApp.route("/data")
# @login_required
# def data():
#     '''data view'''
#     pg_name = "Data" 
#     return render_template("data.html", pg_name=pg_name)

# @restimatorApp.route("/contact")
# def contact():
#     '''contact view'''
#     pg_name = "Contact" 
#     return render_template("contact.html", pg_name=pg_name)

# # @csrf.error_handler
# # def csrf_error(reason):
# #     return render_template('csrf_error.html', reason=reason), 400