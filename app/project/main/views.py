from project import db
from flask import render_template, flash, redirect, url_for, request, Blueprint
from flask.ext.login import login_required
from .sign_up import RegistrationForm
from .analysis import AnalysisForm
from project.models import * 

main_blueprint = Blueprint("main", __name__, template_folder="templates")

###VIEWS: handlers that respond to requests from browsers. Flask handlers are written as functions (each view function is mapped to one or more request URLs)###

@main_blueprint.route("/")
@main_blueprint.route("/home", methods=["GET", "POST"])
@login_required
def home():
    '''home view'''
    pg_name = "Home" 
    random = db.session.query(Users).all()
    return render_template("home.html", pg_name=pg_name, random=random) # function takes a template filename and a variable list of template args and returns the rendered template (invokes Jinja2 templating engine)

@main_blueprint.route("/sign_up", methods=["GET", "POST"])
def sign_up():
    '''Sign up view'''
    pg_name = "Sign Up" 
    form = RegistrationForm() # create instance of RegistrationForm
    if request.method == "POST" and form.validate():
        user = Users(form.username.data, form.password.data) 
        db.session.add(user)
        db.session.commit()
        flash("Successfully Registered")
        return redirect(url_for("home"))
    return render_template("sign_up.html", pg_name=pg_name, form=form)

@main_blueprint.route("/analysis", methods=["GET", "POST"])
@login_required
def analysis():
    '''analysis view'''
    pg_name = "Analysis" 
    form = AnalysisForm()
    query = ""
    if request.method == "POST" and form.validate_on_submit():
        query = Results.query.filter_by(day=form.day.data, time=form.time.data, module=form.module.data).all()
    return render_template("analysis.html", pg_name=pg_name, form=form, query=query)

@main_blueprint.route("/about")
def about():
    '''about view'''
    pg_name = "About" 
    return render_template("about.html", pg_name=pg_name)

@main_blueprint.route("/data")
@login_required
def data():
    '''data view'''
    pg_name = "Data" 
    return render_template("data.html", pg_name=pg_name)

@main_blueprint.route("/contact")
def contact():
    '''contact view'''
    pg_name = "Contact" 
    return render_template("contact.html", pg_name=pg_name)

# @csrf.error_handler
# def csrf_error(reason):
#     return render_template('csrf_error.html', reason=reason), 400