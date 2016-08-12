from flask import render_template, flash, redirect, url_for, request, Blueprint, jsonify
import json
from flask.ext.login import login_required
from .form import AnalysisForm
from project.models import Results
from project.analysis.data_analysis import *
import pandas as pd
import numpy as np
import pickle
from sklearn.linear_model import LinearRegression
from sklearn import metrics
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC

analysis_blueprint = Blueprint("analysis", __name__, template_folder="templates")

@analysis_blueprint.route("/analysis", methods=["GET", "POST"])
@login_required
def analysis():
    '''analysis view'''
    pg_name = "Analysis"
    form = AnalysisForm()
    cate_model = False
    svc = False
    accuracy = None
    model_hist = "" 
    hist = None
    pred = None
    hist_pred = None
    hist_auth = None
    room_cap = None
    chart_1 = "" 
    chart_2 = None
    ave_pred = None
    ave_auth = None
    ave_X = None
    day = None
    time = None
    room = None
    date = None
    
    if form.validate_on_submit():
        # model's accuracy metrics
        query_scores = Results.query.filter_by(model_type=form.model_type.data).with_entities(Results.accuracy).all() # Query to get accuracy scores dictionary of model
        json_acceptable_string = query_scores[0][0].replace("'", "\"") # Convert response into json
        accuracy = json.loads(json_acceptable_string) # accuracy JSON

        # selected model (unpickle)
        query_model = Results.query.filter_by(model_type=form.model_type.data).with_entities(Results.model).all() # Query to get model object
        model = pickle.loads(query_model[0][0]) # load pickled object from db

        df_model = abt().copy() # Create ABT dataframe (Need info from this not needed for analysis)
        df_model = df_model.sort_values(by="time", ascending=1)
        # Get Model Predictions for historical information
        date = str(form.date.data)
        day = get_day(date)
        room = form.room.data
        time = form.time.data
        if "Linear" in form.model_type.data:
            X = df_model["authenticated_client_count"].reshape(len(df_model["authenticated_client_count"]), 1) # Explanatory variable (REPLACE WITH PICKLE)
            model_hist = model.predict(X)
        elif "Support" in form.model_type.data:
            svc = True
            X = df_model["authenticated_client_count"].reshape(len(df_model["authenticated_client_count"]), 1) # Explanatory variable (REPLACE WITH PICKLE)
            model_hist = model.predict(X)
        else:
            cate_model = True
            if "Naive" in form.model_type.data:
                X = df_model["authenticated_client_count"].reshape(len(df_model["authenticated_client_count"]), 1) # Explanatory variable (REPLACE WITH PICKLE)
            elif "Logistic" in form.model_type.data:
                X = df_model["authenticated_client_count"].reshape(len(df_model["authenticated_client_count"]), 1) # Explanatory variable (REPLACE WITH PICKLE)
            elif "Neighbor" in form.model_type.data:
                X = df_model["authenticated_client_count"].reshape(len(df_model["authenticated_client_count"]), 1) # Explanatory variable (REPLACE WITH PICKLE)
            groups = [0, 25, 50, 75, 100] # need to make this dynamic (if we decide to have more percentage groups)
            group_index = model.predict_proba(X).argmax(axis=1)
            model_hist = []
            for i in group_index:
                model_hist.append(groups[i])

        df_model["predicted"] = pd.Series(model_hist, index=df_model.index) # Append historical predictions to ABT
        df_model["predicted"] = df_model["predicted"].apply(lambda x: round(x, 2)) # Round values to two decimal places (IS THIS NEEDED? IF NOT DO ON CLIENT-SIDE)

        location = df_model[(df_model["campus"] == form.campus.data) & (df_model["building"] == form.building.data) & (df_model["room"] == room)].copy() # DF based on location selected
        room_cap = location["capacity"].values[0]
        # CHART 1: Plot historical predictions against ground truth
        df_chart_1 = location[location["date"] == date]
        chart_1 = df_chart_1.to_dict("records") # DF based on date selected & convert df to dict

        # Report variables
        try:
            hist_vars = df_chart_1[df_chart_1["time"] == time]
            hist_pred = hist_vars["predicted"].values[0]
            hist_auth = hist_vars["authenticated_client_count"].values[0]
            hist = True
        except IndexError:
            hist = False
            hist_pred = date + ": No class on in " + room + " at " + time

        # CHART 2: Find the average number of devices per day (day based on the date selected) and use these to predict how many ppl are typically in class
        df_chart_2 = location[(location["day"] == day)].copy() # DF based on day selected
        df_chart_2 = df_chart_2.groupby(["room", "time"], as_index=False).mean() # get the mean values for day selected
        del df_chart_2["predicted"]
        if "Linear" in form.model_type.data:
            X = df_chart_2["authenticated_client_count"].reshape(len(df_chart_2["authenticated_client_count"]), 1) # Explanatory variable (REPLACE WITH PICKLE)
            model_pred = model.predict(X)
        elif "Support" in form.model_type.data:
            X = df_chart_2["authenticated_client_count"].reshape(len(df_chart_2["authenticated_client_count"]), 1) # Explanatory variable (REPLACE WITH PICKLE)
            model_pred = model.predict(X)
        else:
            if "Naive" in form.model_type.data:
                X = df_chart_2["authenticated_client_count"].reshape(len(df_chart_2["authenticated_client_count"]), 1) # Explanatory variable (REPLACE WITH PICKLE)
            elif "Logistic" in form.model_type.data:
                X = df_chart_2["authenticated_client_count"].reshape(len(df_chart_2["authenticated_client_count"]), 1) # Explanatory variable (REPLACE WITH PICKLE)
            elif "Neighbor" in form.model_type.data:
                X = df_chart_2["authenticated_client_count"].reshape(len(df_chart_2["authenticated_client_count"]), 1) # Explanatory variable (REPLACE WITH PICKLE)
            group_index = model.predict_proba(X).argmax(axis=1)
            model_pred = []
            for i in group_index:
                model_pred.append(groups[i])
        df_chart_2["predicted"] = pd.Series(model_pred, index=df_chart_2.index) # Append historical predictions to ABT
        df_chart_2["predicted"] = df_chart_2["predicted"].apply(lambda x: round(x, 2)) # Round values to two decimal places (IS THIS NEEDED? IF NOT DO ON CLIENT-SIDE)
        chart_2 =  df_chart_2.to_dict("records") # convert df to dict

        # Prediction based off average number of devices in room
        try:
            ave_vars = df_chart_2[df_chart_2["time"] == time].copy() 
            ave_auth = ave_vars["authenticated_client_count"].values[0]
            if cate_model == True:
                ave_pred = groups[model.predict_proba(ave_auth).argmax(axis=1)]
            else:
                ave_pred = model.predict(ave_auth)[0]
            pred = True
        except TypeError:
            pred = False
            ave_pred = day + ": No class on in " + room + " at " + time
        except IndexError:
            pred = False
            ave_pred = day + ": No class on in " + room + " at " + time

    return render_template("analysis.html", pg_name=pg_name, form=form, cate_model=cate_model, svc=svc, accuracy=accuracy, pred=pred, hist=hist, model_hist=model_hist, hist_pred=hist_pred, hist_auth=hist_auth, room_cap=room_cap, chart_1=chart_1, chart_2=chart_2, ave_pred=ave_pred, ave_auth=ave_auth, day=day, time=time, room=room, date=date)


