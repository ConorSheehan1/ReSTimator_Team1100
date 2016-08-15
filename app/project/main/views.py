from flask import render_template, Blueprint, jsonify
from flask.ext.login import login_required
from project import db
from project.models import *
# from werkzeug import secure_filename
# from .upload import UploadForm
# from project import app

# values accessable by all pages
main_blueprint = Blueprint("main", __name__, template_folder="templates")

# VIEWS: handlers that respond to requests from browsers.
# Flask handlers are written as functions (each view function is mapped to one or more request URLs)

# make list of tables available to all routes
list_of_tables = [table for table in db.metadata.tables.keys()]
# don't allow access to users or results table
list_of_tables.remove("users")
list_of_tables.remove("results")


def convert_to_nested_dict(obj):
    # get all keys in table
    keys = obj.__table__.columns.keys()

    # get all rows in table
    data = db.session.query(obj).all()

    # for every row in the table, create a dictionary entry which is itself a dictionary of values for that row
    nested_dicts = {i: {key: getattr(data[i], key) for key in keys} for i in range(len(data))}
    return nested_dicts


@main_blueprint.route("/")
@main_blueprint.route("/home", methods=["GET", "POST"])
def home():
    '''home view'''
    pg_name = "Home" 
    # random = db.session.query(Users).all()
    # return render_template("home.html", pg_name=pg_name, random=random)
    return render_template("home.html", pg_name=pg_name)
    # function takes a template filename and a variable list of template args and returns the rendered template
    #  (invokes Jinja2 templating engine)


@main_blueprint.route("/api", methods=["GET", "POST"])
@login_required
def api():
    usage = ["How to use:", "Add api followed by name of the table you want to query to the url, or use the links below.",
             "List of available tables:"]
    return render_template("api.html", pg_name="api", usage=usage, list_of_tables=list_of_tables)


@main_blueprint.route("/api/<table_name>", methods=["GET", "POST"])
@login_required
def api_results(table_name):
    # if table_name not in list_of_tables:
    #     error = ["We didn't recognise that table name.", "Please try one of these:"]
    #     return render_template('404.html', pg_name="error", error=error, list_of_tables=list_of_tables), 404

    # table_name = table_name[0].upper() + table_name[1:]
    # table = exec("%s" % table_name)

    if table_name == "location":
        table = Location
    elif table_name == "module":
        table = Module
    elif table_name == "occupy":
        table = Occupy
    else:
        error = ["We didn't recognise that table name.", "Please try one of these:"]
        return render_template('404.html', pg_name="error", error=error, list_of_tables=list_of_tables), 404

    return jsonify(convert_to_nested_dict(table))


# __andy's stuff__

# @csrf.error_handler
# def csrf_error(reason):
#     return render_template('csrf_error.html', reason=reason), 400