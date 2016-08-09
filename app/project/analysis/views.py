from flask import render_template, flash, redirect, url_for, request, Blueprint, jsonify
import json
from flask.ext.login import login_required
from .form import AnalysisForm
from project import db
from project.models import Results
from project.analysis.data_analysis import *
import pandas as pd
import sqlite3
import numpy as np
import pickle
from sklearn.linear_model import LinearRegression
from sklearn import metrics
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC


analysis_blueprint = Blueprint("analysis", __name__, template_folder="templates")

# VIEWS: handlers that respond to requests from browsers.
# Flask handlers are written as functions (each view function is mapped to one or more request URLs)

@analysis_blueprint.route("/analysis", methods=["GET", "POST"])
@login_required
def analysis():
    '''analysis view'''
    pg_name = "Analysis"
    # Forms:
    form = AnalysisForm()

    accuracy = ""
    day_pred = ""
    df_chart_1 = ""

    cate_model = False
    svc = False

    if form.validate_on_submit():
        query_scores = Results.query.filter_by(model_type=form.model_type.data).with_entities(Results.accuracy).all() # Query to get accuracy scores dictionary of model

        json_acceptable_string = query_scores[0][0].replace("'", "\"") # Convert response into json
        accuracy = json.loads(json_acceptable_string) # accuracy dictionary

        query_model = Results.query.filter_by(model_type=form.model_type.data).with_entities(Results.model).all() # Query to get model object
        model = pickle.loads(query_model[0][0]) # load pickled object form db

        conn = sqlite3.connect("./project/sample.db") # db connection
        df_model = abt(conn).copy() # ABT
        conn.close() # close db connection
        X = df_model["authenticated_client_count"].reshape(len(df_model["authenticated_client_count"]), 1) # Explanatory variable
        
        # Predictions from model
        if "Linear" not in form.model_type.data and "Support" not in form.model_type.data:
            cate_model = True
            groups = [0, 25, 50, 75, 100] # need to make this dynamic (if we decide to have more percentage groups)
            group_index = model.predict_proba(X).argmax(axis=1)
            m = []
            for i in group_index:
                m.append(groups[i])
            model = m
        else:
            model = model.predict(X)

        if "Support" in form.model_type.data:
            svc = True
        
        df_model["predicted"] = pd.Series(model, index=df_model.index)
        df_model["predicted"] = df_model["predicted"].apply(lambda x: round(x, 2))
        df_model = df_model.sort_values(by="time", ascending=1)


        campus = form.campus.data
        building = form.building.data
        room = form.room.data
        df_location = df_model[(df_model["campus"] == campus) & (df_model["building"] == building) & (df_model["room"] == room)].copy()

        try:
            model_pred = df_location[(df_location["day"] == form.day.data) & (df_location["time"] == form.time.data)].copy().values[0][-1]
            print(model_pred)
        except IndexError:
            model_pred = "N/A"
        # Chart
        df_chart_1 = df_location[df_model["day"] == form.day.data].to_dict("records")

    return render_template("analysis.html", pg_name=pg_name, form=form, day_pred=day_pred, df_chart_1=df_chart_1, accuracy=accuracy, cate_model=cate_model, svc=svc)

# @analysis_blueprint.route("/analysis", methods=["GET", "POST"])
# @login_required
# def analysis():
#     '''analysis view'''
#     pg_name = "Analysis"
    
#     form = AnalysisForm()
#     model_pred = ""
#     accuracy = ""
#     df_model = ""
#     cate_model = False
#     svc = False
#     if request.method == "POST" and form.validate_on_submit():
#         # Dictionary: accuracy score
#         query = Results.query.filter_by(model_type=form.model_type.data).with_entities(Results.accuracy).all() # Query to get accuracy scores of model

#         json_acceptable_string = query[0][0].replace("'", "\"") # Convert response into json
#         accuracy = json.loads(json_acceptable_string) # accuracy dictionary

#         # Model
#         query_model = Results.query.filter_by(model_type=form.model_type.data).with_entities(Results.model).all() # Query to get model object
#         model = pickle.loads(query_model[0][0])

#         conn = sqlite3.connect("./project/sample.db") # db connection
#         df_model = abt(conn).copy() # ABT
#         conn.close() # close db connection
#         X = df_model["authenticated_client_count"].reshape(len(df_model["authenticated_client_count"]), 1)
        
#         # Get predictions from model
#         if "Linear" not in form.model_type.data and "Support" not in form.model_type.data:
#             cate_model = True
#             groups = [0, 25, 50, 75, 100] # need to make this dynamic (if we decide to have more percentage groups)
#             group_index = model.predict_proba(X).argmax(axis=1)
#             m = []
#             for i in group_index:
#                 # print(m)
#                 m.append(groups[i])
#             model = m
#         else:
#             model = model.predict(X)

#         if "Support" in form.model_type.data:
#             svc = True
        
#         df_model["predicted"] = pd.Series(model, index=df_model.index)
#         df_model["predicted"] = df_model["predicted"].apply(lambda x: round(x, 2))

#         try:
#             model_pred = df_model[(df_model["room"] == form.room.data) & (df_model["day"] == form.day.data) & (df_model["time"] == form.time.data)].copy().values[0][-1]
#         except IndexError:
#             model_pred = "N/A"
            
#         df_model = df_model.sort_values(by="time", ascending=1)

#         df_model = df_model[(df_model["room"] == form.room.data) & (df_model["day"] == form.day.data)].to_dict("records")

#     return render_template("analysis.html", pg_name=pg_name, form=form, model_pred=model_pred, accuracy=accuracy, df_model=df_model, cate_model=cate_model, svc=svc)