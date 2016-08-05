from project import db
from project.models import Results
from project.analysis.data_analysis import *
import pandas as pd
import sqlite3
import numpy as np
import pickle
from sklearn.linear_model import LinearRegression
# from sklearn.cross_validation import train_test_split
# from sklearn.cross_validation import cross_val_score
from sklearn import metrics
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC

conn = sqlite3.connect("./project/sample.db") # db connection
# ABTs for each model
df_lr = abt(conn).copy() # y: occupancy number, X: auth. client count
df_log = abt(conn, normal=False, convert=True).copy() # y: occupancy category, X: auth. client count
df_gnb = abt(conn, normal=False, convert=True).copy() # y: occupancy category, X: auth. client count
df_knn = abt(conn, normal=False, convert=True).copy() # y: occupancy category, X: auth. client count
df_svm = abt(conn, normal=False, convert=True).copy() # y: occupancy category, X: auth. client count

conn.close() # close db connection


##### Model 1: Simple Linear Regression #####
lr = LinearRegression()
X = df_lr["authenticated_client_count"].reshape(len(df_lr["authenticated_client_count"]), 1)
y = df_lr["min_occ_reg"]

lr.fit(X, y) # Fit the model 
lr_model = pickle.dumps(lr) # variable containing model object 

# Create dictionary of accuracy measures
pred_lr = lr.predict(X)
lr_dict = {"Mean Squared Error": metrics.mean_squared_error(y, pred_lr), "Root Mean Squared Error": np.sqrt(metrics.mean_squared_error(y, pred_lr)), "R squared": lr.score(X, y)}

# Commit to database
LinearModel = Results(model_type="Simple Linear Regression", model=lr_model, accuracy=str(lr_dict)) 
db.session.add(LinearModel)
db.session.commit()


##### Model 2: Multinomial Logistic Regression #####
log = LogisticRegression()
X = df_log["authenticated_client_count"].reshape(len(df_log["authenticated_client_count"]), 1)
y = df_log["occupancy"]

log.fit(X.astype(int), y) # Fit the model 
log_model = pickle.dumps(log) # variable containing model object 

# Create dictionary of accuracy measures
pred_log = log.predict(X)
log_dict = {"Accuracy Classification Score": metrics.accuracy_score(y, pred_log), "Precision Score": metrics.precision_score(y, pred_log, average="macro"), "Recall Score": metrics.recall_score(y, pred_log, average="macro"), "F-score": metrics.f1_score(y, pred_log, average="macro")}

# Commit to database
LogisticRegression = Results(model_type="Multinomial Logistic Regression", model=log_model, accuracy=str(log_dict)) 
db.session.add(LogisticRegression)
db.session.commit()


# ##### Model 3: Gaussian Naive Bayes #####
gnb = GaussianNB()
X = df_gnb["authenticated_client_count"].reshape(len(df_gnb["authenticated_client_count"]), 1)
y = df_gnb["occupancy"]

gnb.fit(X, y) # Fit the model 
gnb_model = pickle.dumps(gnb) # variable containing model object 

# Create dictionary of accuracy measures
pred_gnb = gnb.predict(X)
gnb_dict = {"Accuracy Classification Score": metrics.accuracy_score(y, pred_gnb), "Precision Score": metrics.precision_score(y, pred_gnb, average="macro"), "Recall Score": metrics.recall_score(y, pred_gnb, average="macro"), "F-score": metrics.f1_score(y, pred_gnb, average="macro")}

# Commit to database
GaussianNB = Results(model_type="Gaussian Naive Bayes", model=gnb_model, accuracy=str(gnb_dict)) 
db.session.add(GaussianNB)
db.session.commit()


# ##### Model 4: k-Nearest Neighbor #####
knn = KNeighborsClassifier()
X = df_knn["authenticated_client_count"].reshape(len(df_knn["authenticated_client_count"]), 1)
y = df_knn["occupancy"]

knn.fit(X, y) # Fit the model 
knn_model = pickle.dumps(knn) # variable containing model object 

# Create dictionary of accuracy measures
pred_knn = knn.predict(X)
knn_dict = {"Accuracy Classification Score": metrics.accuracy_score(y, pred_knn), "Precision Score": metrics.precision_score(y, pred_knn, average="macro"), "Recall Score": metrics.recall_score(y, pred_knn, average="macro"), "F-score": metrics.f1_score(y, pred_knn, average="macro")}

# Commit to database
KNeighborsClassifier = Results(model_type="k-Nearest Neighbor", model=knn_model, accuracy=str(knn_dict)) 
db.session.add(KNeighborsClassifier)
db.session.commit()


# ##### Model 5: Support Vector Machines #####
svc = SVC()
X = df_svm["authenticated_client_count"].reshape(len(df_svm["authenticated_client_count"]), 1)
y = df_svm["occupancy"]

svc.fit(X, y) # Fit the model 
svc_model = pickle.dumps(svc) # variable containing model object 

# Create dictionary of accuracy measures
pred_svc = svc.predict(X)
svc_dict = {"Accuracy Classification Score": metrics.accuracy_score(y, pred_svc), "Precision Score": metrics.precision_score(y, pred_svc, average="macro"), "Recall Score": metrics.recall_score(y, pred_svc, average="macro"), "F-score": metrics.f1_score(y, pred_svc, average="macro")}

# Commit to database
SVC = Results(model_type="Support Vector Machines", model=svc_model, accuracy=str(svc_dict)) 
db.session.add(SVC)
db.session.commit()






