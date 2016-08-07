from flask import render_template, Blueprint, jsonify
from flask.ext.login import login_required
from project import db
from project.models import *
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
        error = ["We didn't recognise that table name.", "Please try one of these:"]
        return render_template('404.html', pg_name="error", error=error, list_of_tables=list_of_tables), 404

    def convert_to_json(obj):
        # sort of works
        # data = dict((column, str(getattr(obj, column))) for column in obj.__table__.columns.keys())
        nested_dicts = []

        keys = obj.__table__.columns.keys()
        data = db.session.query(obj).all()

        print("?????????\n", list((getattr(data[0], column)) for column in obj.__table__.columns.keys()))

        print("!!!!!!!\n", type(data), len(data), type(data[0]))
        for i in range(len(data)):
            # for every row in db, convert that row to a dictionary, then jsonify it
            # nested_dicts.append({key: getattr(data[i], key) for key in keys})

            nested_dicts.append(jsonify({key: getattr(data[i], key) for key in keys}))

        print(nested_dicts)
        return jsonify(nested_dicts)

        # data = dict((column, getattr(obj, column)) for column in obj.__table__.columns.keys())
        # for key in data.keys():
        #     print("!!!", data[key].all())
        # return data

    print(convert_to_json(Location))
    # print(db.session.query(Occupy).all())
    # return jsonify(convert_to_dict(Occupy))

    return jsonify(dict((column, str(getattr(Location, column))) for column in Location.__table__.columns.keys()))

# # capitalise first letter
# table_name = table_name[0].upper() + table_name[1:]

# # convert string into variable
# table = exec("%s" % table_name)
# print("\n\n\n\n\n!!!!!!!!!!!!!!!!!!!!\n\n\n", table_name, table)

# data = db.session.query(Occupy).all()

# sort of works
# data = {c.name: str(getattr(Occupy, c.name)) for c in Occupy.__table__.columns}


# data = jsonify({c.name: str(getattr(Occupy, c.name)) for c in Occupy.__table__.columns})
# print("!!!!!!!!!!!!!!!!!!!!!!!!\n", data)
# return data
# # return json.dumps(dict(data))


# __andy's stuff__


# @csrf.error_handler
# def csrf_error(reason):
#     return render_template('csrf_error.html', reason=reason), 400