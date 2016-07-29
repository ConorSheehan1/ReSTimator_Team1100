from flask import render_template, flash, redirect, url_for, request, Blueprint
from flask.ext.login import login_required
from project import db
from project.models import * 

main_blueprint = Blueprint("main", __name__, template_folder="templates")

# VIEWS: handlers that respond to requests from browsers.
# Flask handlers are written as functions (each view function is mapped to one or more request URLs)


@main_blueprint.route("/")
@main_blueprint.route("/home", methods=["GET", "POST"])
@login_required
def home():
    '''home view'''
    pg_name = "Home" 
    random = db.session.query(Users).all()
    return render_template("home.html", pg_name=pg_name, random=random)
    # function takes a template filename and a variable list of template args and returns the rendered template
    #  (invokes Jinja2 templating engine)

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