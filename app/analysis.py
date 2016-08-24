from project import db
from project.models import Results
from project.analysis.data_analysis import *
import pandas as pd
import numpy as np
import pickle
from sklearn.linear_model import LinearRegression
from sklearn.cross_validation import train_test_split
from sklearn.cross_validation import cross_val_score
from sklearn import metrics
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC

def cate_exp_var(df):
    '''Input: GT percentages, Output: Array of coordinates i.e. no. of people occupying a room based on GT and client count'''
    occ = df["occupancy"].copy().apply(lambda x: (x / 100) * df["capacity"].values[0])
    EXP = []
    for a, o in zip(df["authenticated_client_count"], occ):
        EXP.append([a, o])
    return np.array(EXP)


def analysis():
    # Delete existing data in table
    db.session.query(Results).delete()
    db.session.commit()

    # ABTs for each model
    df_lr = abt().copy() 
    df_log = abt(normal=False, convert=True).copy() # normal is false because it removes a category group
    df_gnb = abt(normal=False, convert=True).copy() # normal is false because it removes a category group
    df_knn = abt(normal=False, convert=True).copy() # normal is false because it removes a category group
    df_svm = abt(normal=False, convert=True).copy() # normal is false because it removes a category group
    
    ##### Model 1: Simple Linear Regression #####
    lr = LinearRegression() # model object
    # Explanatory Variable
    X = df_lr["authenticated_client_count"].reshape(len(df_lr["authenticated_client_count"]), 1)
    model_exp_var = pickle.dumps(X)
    # Dependent Variable
    y = df_lr["min_occ_reg"]
    # Fit model, predict and cross eval 
    lr.fit(X, y) 
    lr_model = pickle.dumps(lr) 
    pred_lr = lr.predict(X)
    df_lr["predicted"] = pd.Series(pred_lr, index=df_lr.index) # Append historical predictions to ABT
    abt_lr = pickle.dumps(df_lr)
    cross_val_scores = cross_val_score(lr.fit(X, y), X.astype(int), y.astype(int), cv=5)
    # Create dictionary of accuracy measures
    lr_dict = {"Mean Squared Error": metrics.mean_squared_error(y, pred_lr), "Root Mean Squared Error": np.sqrt(metrics.mean_squared_error(y, pred_lr)), "R squared": lr.score(X, y), "Cross Val. Accuracy (+/- %0.2f)" % (cross_val_scores.std() * 2): cross_val_scores.mean()}
    # Commit to database
    LinearModel = Results(abt=abt_lr, model_type="Simple Linear Regression", model=lr_model, accuracy=str(lr_dict)) 
    db.session.add(LinearModel)
    db.session.commit()

    ##### Model 2: Multinomial Logistic Regression #####
    # Explanatory Variable: Coordinates of auth client count and ground truth (no. of ppl)
    X = cate_exp_var(df_log)
    model_exp_var = pickle.dumps(X)
    # Dependent Variable
    y = df_log["occupancy"] # categories 
    # Find best number of neighbours based on train and test scores
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=42)
    regularisation = ["l1", "l2"]
    scores=[]
    for p in regularisation:
        clf = LogisticRegression(penalty=p).fit(X_train, y_train)
        scores.append(round(clf.score(X_test, y_test),2))
    penalty = regularisation[scores.index(max(scores))]
    log = LogisticRegression(penalty=penalty)
    # Fit model, predict and cross eval 
    log.fit(X, y) 
    log_model = pickle.dumps(log) # variable containing model object 
    pred_log = log.predict(X)
    df_log["predicted"] = pd.Series(pred_log, index=df_log.index) # Append historical predictions to ABT
    abt_log = pickle.dumps(df_log)
    # Create dictionary of accuracy measures
    scores = cross_val_score(log, X, y, cv=5)
    clf = LogisticRegression().fit(X_train, y_train)
    pred_log_train = clf.predict(X_test)
    # Create dictionary of accuracy measures
    log_dict = {"Accuracy Classification Score": metrics.accuracy_score(y_test, pred_log_train), "Precision Score": metrics.precision_score(y_test, pred_log_train, average="macro"), "Recall Score": metrics.recall_score(y_test, pred_log_train, average="macro"), "F-score": metrics.f1_score(y_test, pred_log_train, average="macro"), "Cross Val. Accuracy (+/- %0.2f)" % (scores.std() * 2): scores.mean()}
    # Commit to database
    Logistic_Regression = Results(abt=abt_log, model_type="Multinomial Logistic Regression", model=log_model, accuracy=str(log_dict)) 
    db.session.add(Logistic_Regression)
    db.session.commit()
    
    ##### Model 3: Gaussian Naive Bayes #####
    gnb = GaussianNB() 
    # Explanatory Variable: Coordinates of auth client count and ground truth (no. of ppl)
    X = cate_exp_var(df_gnb)
    model_exp_var = pickle.dumps(X)
    # Dependent Variable
    y = df_gnb["occupancy"]

    # Fit model, predict and cross eval 
    gnb.fit(X, y) # Fit the model 
    gnb_model = pickle.dumps(gnb) # variable containing model object 
    pred_gnb = gnb.predict(X)
    df_gnb["predicted"] = pd.Series(pred_gnb, index=df_gnb.index) # Append historical predictions to ABT
    abt_gnb = pickle.dumps(df_gnb)
    # Create dictionary of accuracy measures
    scores = cross_val_score(gnb, X, y, cv=5)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=42)
    clf = GaussianNB().fit(X_train, y_train)
    pred_gnb_train = clf.predict(X_test)
    gnb_dict = {"Accuracy Classification Score": metrics.accuracy_score(y_test, pred_gnb_train), "Precision Score": metrics.precision_score(y_test, pred_gnb_train, average="macro"), "Recall Score": metrics.recall_score(y_test, pred_gnb_train, average="macro"), "F-score": metrics.f1_score(y_test, pred_gnb_train, average="macro"), "Cross Val. Accuracy (+/- %0.2f)" % (scores.std() * 2): scores.mean()}
    # Commit to database
    Gaussian_NB = Results(abt=abt_gnb, model_type="Gaussian Naive Bayes", model=gnb_model, accuracy=str(gnb_dict)) 
    db.session.add(Gaussian_NB)
    db.session.commit()

    ##### Model 4: k-Nearest Neighbor #####
    # Explanatory Variable: Coordinates of auth client count and ground truth (no. of ppl)
    X = cate_exp_var(df_knn)
    model_exp_var = pickle.dumps(X)
    # Dependent Variable
    y = df_knn["occupancy"]
    # Find best number of neighbours based on train and test scores
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=42)
    scores=[]
    for n in range(2,15):
        clf = KNeighborsClassifier(n_neighbors=n).fit(X_train, y_train)
        scores.append(round(clf.score(X_test, y_test),2))
    neighbours = scores.index(max(scores)) + 1
    knn = KNeighborsClassifier(n_neighbors=neighbours)
    # Fit model, predict and cross eval 
    knn.fit(X, y) 
    knn_model = pickle.dumps(knn) # variable containing model object 
    pred_knn = knn.predict(X)
    df_knn["predicted"] = pd.Series(pred_knn, index=df_knn.index) # Append historical predictions to ABT
    abt_knn = pickle.dumps(df_knn)
    # Create dictionary of accuracy measures
    scores = cross_val_score(knn, X, y, cv=5)
    clf = knn.fit(X_train, y_train)
    pred_knn_train = clf.predict(X_test)
    knn_dict = {"Accuracy Classification Score": metrics.accuracy_score(y_test, pred_knn_train), "Precision Score": metrics.precision_score(y_test, pred_knn_train, average="macro"), "Recall Score": metrics.recall_score(y_test, pred_knn_train, average="macro"), "F-score": metrics.f1_score(y_test, pred_knn_train, average="macro"), "Cross Val. Accuracy (+/- %0.2f)" % (scores.std() * 2): scores.mean()}
    # Commit to database
    KNeighbors_Classifier = Results(abt=abt_knn, model_type="k-Nearest Neighbor", model=knn_model, accuracy=str(knn_dict)) 
    db.session.add(KNeighbors_Classifier)
    db.session.commit()

    ##### Model 5: Support Vector Machines ##### 
    # Explanatory Variable: Coordinates of auth client count and ground truth (no. of ppl)
    X = cate_exp_var(df_svm)
    model_exp_var = pickle.dumps(X.copy())
    # Dependent Variable
    y = df_svm["occupancy"]
    # Find best number of for gamma based on train and test scores
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=42)
    scores=[]
    for n in range(0,20):
        clf = SVC(gamma=n).fit(X_train, y_train)
        scores.append(round(clf.score(X_test, y_test),2))
    gamma = scores.index(max(scores))
    svc = SVC(gamma=gamma)
    # Fit model, predict and cross eval 
    svc.fit(X, y) # Fit the model 
    svc_model = pickle.dumps(svc) # variable containing model object 
    pred_svc = svc.predict(X)
    df_svm["predicted"] = pd.Series(pred_svc, index=df_svm.index) # Append historical predictions to ABT
    abt_svc = pickle.dumps(df_svm)
    # Create dictionary of accuracy measures
    scores = cross_val_score(svc, X, y, cv=5)
    clf = svc.fit(X_train, y_train)
    pred_svc_train = clf.predict(X_test)
    svc_dict = {"Accuracy Classification Score": metrics.accuracy_score(y_test, pred_svc_train), "Precision Score": metrics.precision_score(y_test, pred_svc_train, average="macro"), "Recall Score": metrics.recall_score(y_test, pred_svc_train, average="macro"), "F-score": metrics.f1_score(y_test, pred_svc_train, average="macro"), "Cross Val. Accuracy (+/- %0.2f)" % (scores.std() * 2): scores.mean()}
    # Commit to database
    SVC_results = Results(abt=abt_svc, model_type="Support Vector Machines", model=svc_model, accuracy=str(svc_dict)) 
    db.session.add(SVC_results)
    db.session.commit()

if __name__ == "__main__":
    analysis()