from flask import render_template, Blueprint
from flask.ext.login import login_required
from project import db
from project.models import *
import json
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

# make list of tables available to all routes
list_of_tables = [table for table in db.metadata.tables.keys()]
# make sure not to show that a users table exists
list_of_tables.remove("users")

@main_blueprint.route("/api", methods=["GET", "POST"])
@login_required
def api():
    usage = ["Usage:", "Add the name of the table you want to query to the url.", "List of available tables:"]
    return render_template("api.html", pg_name="api", usage=usage, list_of_tables=list_of_tables)


@main_blueprint.route("/api/<table_name>", methods=["GET", "POST"])
@login_required
def api_results(table_name):
    if table_name not in list_of_tables:
        error = ["We didn't recognise that table name", "Please try one of these:"]
        return render_template('404.html', error=error, list_of_tables=list_of_tables), 404
    # data = db.session.table_name
    return table_name


# @csrf.error_handler
# def csrf_error(reason):
#     return render_template('csrf_error.html', reason=reason), 400