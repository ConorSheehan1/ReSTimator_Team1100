from flask import render_template, flash, redirect, url_for, request, Blueprint
from flask.ext.login import login_required
from .form import AnalysisForm
from project import db
from project.models import Results

analysis_blueprint = Blueprint("analysis", __name__, template_folder="templates")

# VIEWS: handlers that respond to requests from browsers.
# Flask handlers are written as functions (each view function is mapped to one or more request URLs)

@analysis_blueprint.route("/analysis", methods=["GET", "POST"])
@login_required
def analysis():
    '''analysis view'''
    pg_name = "Analysis"
    form = AnalysisForm()
    query = ""
    chart_query = ""
    if request.method == "POST" and form.validate_on_submit():
        query = Results.query.filter_by(room=form.room.data, day=form.day.data, time=form.time.data).all()
        chart_query = Results.query.filter_by(room=form.room.data, day=form.day.data)
    return render_template("analysis.html", pg_name=pg_name, form=form, query=query, chart_query=chart_query)