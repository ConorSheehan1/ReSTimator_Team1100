from flask import render_template, Blueprint
from flask.ext.login import login_required
# from project import db
# from project.models import *
# from werkzeug import secure_filename
# from .upload import UploadForm
# from project import restimatorApp


main_blueprint = Blueprint("main", __name__, template_folder="templates")

# VIEWS: handlers that respond to requests from browsers.
# Flask handlers are written as functions (each view function is mapped to one or more request URLs)


@main_blueprint.route("/")
@main_blueprint.route("/home", methods=["GET", "POST"])
@login_required
def home():
    '''home view'''
    pg_name = "Home" 
    # random = db.session.query(Users).all()
    # return render_template("home.html", pg_name=pg_name, random=random)
    return render_template("home.html", pg_name=pg_name)
    # function takes a template filename and a variable list of template args and returns the rendered template
    #  (invokes Jinja2 templating engine)


# @csrf.error_handler
# def csrf_error(reason):
#     return render_template('csrf_error.html', reason=reason), 400