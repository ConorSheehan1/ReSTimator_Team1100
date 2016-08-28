from flask import render_template, Blueprint
import json
from flask.ext.login import login_required
from .form import AnalysisForm
from project.models import Results
from project.analysis.data_analysis import *
import pandas as pd
import numpy as np
import pickle

analysis_blueprint = Blueprint("analysis", __name__, template_folder="templates")


@analysis_blueprint.route("/analysis", methods=["GET", "POST"])
@login_required
def analysis():
    '''analysis view'''
    pg_name = "Analysis"
    form = AnalysisForm()
    cate_model = True
    svc = False
    accuracy = None
    hist = None
    pred = None
    hist_pred = None
    hist_auth = None
    room_cap = None
    chart_1 = "" 
    chart_2 = None
    ave_pred = None
    ave_auth = None
    day = None
    time = None
    room = None
    date = None
    df_abt = abt(normal=False, adjust=False).copy() 
    
    if form.validate_on_submit():
        # model's accuracy metrics
        query_scores = Results.query.filter_by(model_type=form.model_type.data).with_entities(Results.accuracy).all() # Query to get accuracy scores dictionary of model
        json_acceptable_string = query_scores[0][0].replace("'", "\"") # Convert response into json
        accuracy = json.loads(json_acceptable_string) # accuracy JSON

        # selected model (unpickle)
        query_model = Results.query.filter_by(model_type=form.model_type.data).with_entities(Results.model).all() # Query to get model object
        model = pickle.loads(query_model[0][0]) # load pickled object from db

        if "Linear" in form.model_type.data:
            cate_model = False
            X = lin_exp_var(df_abt) 
        elif "Logistic" in form.model_type.data:
            X = log_exp_var(df_abt)
        elif "Naive" in form.model_type.data:
            X = gnb_exp_var(df_abt) 
        elif "Neighbor" in form.model_type.data:
            X = knn_exp_var(df_abt) 
        else:
            svc = True
            X = svm_exp_var(df_abt) 
        prediction1 = model.predict(X)
        df_abt["predicted"] = pd.Series(prediction1, index=df_abt.index) # Append predictions to ABT
        df_abt["predicted"] = df_abt["predicted"].apply(lambda x: round(x, 2)) 
        df_abt = df_abt.sort_values(by="time", ascending=1)

        date = str(form.date.data)
        day = get_day(date)
        room = form.room.data
        time = form.time.data

        location = df_abt[(df_abt["campus"] == form.campus.data) & (df_abt["building"] == form.building.data) & (df_abt["room"] == room)].copy() # DF based on location selected
        room_cap = location["capacity"].values[0]

        # CHART 1: Plot historical predictions against ground truth
        df_chart_1 = location[location["date"] == date]
        chart_1 = df_chart_1.to_dict("records") # DF based on date selected & convert df to dict
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
            X = lin_exp_var(df_chart_2) 
        elif "Logistic" in form.model_type.data:
            X = log_exp_var(df_chart_2)
        elif "Naive" in form.model_type.data:
            X = gnb_exp_var(df_chart_2) 
        elif "Neighbor" in form.model_type.data:
            X = knn_exp_var(df_chart_2) 
        else:
            X = svm_exp_var(df_chart_2) 
        prediction2 = model.predict(X)
        df_chart_2["predicted"] = pd.Series(prediction2, index=df_chart_2.index) # Prediction based off average number of devices in room
        df_chart_2["predicted"] = df_chart_2["predicted"].apply(lambda x: round(x, 2)) 
        chart_2 =  df_chart_2.to_dict("records") # convert df to dict

        try:
            ave_vars = df_chart_2[df_chart_2["time"] == time]
            ave_pred = ave_vars["predicted"].values[0]
            ave_auth = ave_vars["authenticated_client_count"].values[0]
            pred = True
        except IndexError:
            pred = False
            ave_pred = day + ": No class on in " + room + " at " + time

    return render_template("analysis.html", pg_name=pg_name, form=form, cate_model=cate_model, svc=svc, accuracy=accuracy, pred=pred, hist=hist, hist_pred=hist_pred, hist_auth=hist_auth, room_cap=room_cap, chart_1=chart_1, chart_2=chart_2, ave_pred=ave_pred, ave_auth=ave_auth, day=day, time=time, room=room, date=date)