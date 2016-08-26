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
    df_lr = abt(normal=False).copy() 
    df_log = abt(normal=False, convert=True).copy() # normal is false because it removes a category group
    df_gnb = abt(normal=False, convert=True).copy() # normal is false because it removes a category group
    df_knn = abt(normal=False, convert=True).copy() # normal is false because it removes a category group
    df_svm = abt(normal=False, convert=True).copy() # normal is false because it removes a category group
    ####################################################
    ##### Model 1: Simple Linear Regression ############
    ####################################################
    lr = LinearRegression() # model object
    
    X = lin_exp_var(df_lr) # Explanatory Variable
    y = df_lr["min_occ_reg"] # Dependent Variable
    # Fit model, predict and cross eval 
    clf = lr.fit(X, y) 
    lr_model = pickle.dumps(clf) 
    
    # Create dictionary of accuracy measures
    pred_lr = clf.predict(X)
    cross_val_scores = cross_val_score(lr, X.astype(int), y.astype(int), cv=5)
    lr_dict = {"Mean Squared Error": metrics.mean_squared_error(y, pred_lr), "Root Mean Squared Error": np.sqrt(metrics.mean_squared_error(y, pred_lr)), "R squared": lr.score(X, y), "Cross Val. Accuracy (+/- %0.2f)" % (cross_val_scores.std()): cross_val_scores.mean()}
    # Commit to database
    LinearModel = Results(model_type="Simple Linear Regression", model=lr_model, accuracy=str(lr_dict)) 
    db.session.add(LinearModel)
    db.session.commit()

    ####################################################
    ##### Model 2: Multinomial Logistic Regression #####
    ####################################################
    log = LogisticRegression()
    
    X = log_exp_var(df_log) # Explanatory Variable: 
    y = df_log["occupancy"] # Dependent Variable
    clf = log.fit(X, y) 
    log_model = pickle.dumps(clf) # variable containing model object 
    
    # Create dictionary of accuracy measures
    pred_log = clf.predict(X)
    scores = cross_val_score(log, X, y, cv=5)
    log_dict = {"Accuracy Classification Score": metrics.accuracy_score(y, pred_log), "Precision Score": metrics.precision_score(y, pred_log, average="macro"), "Recall Score": metrics.recall_score(y, pred_log, average="macro"), "F-score": metrics.f1_score(y, pred_log, average="macro"), "Cross Val. Accuracy (+/- %0.2f)" % (scores.std() * 2): scores.mean()}
    # Commit to database
    Logistic_Regression = Results(model_type="Multinomial Logistic Regression", model=log_model, accuracy=str(log_dict)) 
    db.session.add(Logistic_Regression)
    db.session.commit()
    
    ####################################################
    ##### Model 3: Gaussian Naive Bayes ################
    ####################################################
    gnb = GaussianNB() 

    X = gnb_exp_var(df_gnb)
    y = df_gnb["occupancy"] # Dependent Variable
    # Fit model, predict and cross eval 
    clf = gnb.fit(X, y) # Fit the model 
    gnb_model = pickle.dumps(clf) 
    
    # Create dictionary of accuracy measures
    pred_gnb = clf.predict(X)
    scores = cross_val_score(gnb, X, y, cv=5)
    gnb_dict = {"Accuracy Classification Score": metrics.accuracy_score(y, pred_gnb), "Precision Score": metrics.precision_score(y, pred_gnb, average="macro"), "Recall Score": metrics.recall_score(y, pred_gnb, average="macro"), "F-score": metrics.f1_score(y, pred_gnb, average="macro"), "Cross Val. Accuracy (+/- %0.2f)" % (scores.std() * 2): scores.mean()}
    # Commit to database
    Gaussian_NB = Results(model_type="Gaussian Naive Bayes", model=gnb_model, accuracy=str(gnb_dict)) 
    db.session.add(Gaussian_NB)
    db.session.commit()

    ####################################################
    ##### Model 4: k-Nearest Neighbor ##################
    ####################################################
    X = knn_exp_var(df_knn) # Explanatory Variable:
    y = df_knn["occupancy"] # Dependent Variable
    # Find best number of neighbours based on train and test scores
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=42)
    scores=[]
    for n in range(2,15):
        test = KNeighborsClassifier(n_neighbors=n).fit(X_train, y_train)
        scores.append(round(test.score(X_test, y_test),2))
    neighbours = scores.index(max(scores)) + 2 # index 0 is k=2
    knn = KNeighborsClassifier(n_neighbors=neighbours)
    
    # Fit model, predict and cross eval 
    clf = knn.fit(X, y) 
    knn_model = pickle.dumps(clf) # variable containing model object 
    
    # Create dictionary of accuracy measures
    pred_knn = clf.predict(X)
    scores = cross_val_score(knn, X, y, cv=5)
    knn_dict = {"Accuracy Classification Score": metrics.accuracy_score(y, pred_knn), "Precision Score": metrics.precision_score(y, pred_knn, average="macro"), "Recall Score": metrics.recall_score(y, pred_knn, average="macro"), "F-score": metrics.f1_score(y, pred_knn, average="macro"), "Cross Val. Accuracy (+/- %0.2f)" % (scores.std() * 2): scores.mean()}
    # Commit to database
    KNeighbors_Classifier = Results(model_type="k-Nearest Neighbor", model=knn_model, accuracy=str(knn_dict)) 
    db.session.add(KNeighbors_Classifier)
    db.session.commit()

    ####################################################
    ##### Model 5: Support Vector Machines #############
    #################################################### 
    X = svm_exp_var(df_svm) # Explanatory Variable
    y = df_svm["occupancy"] # Dependent Variable
    # Find best number of for gamma based on train and test scores
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=42)
    scores=[]
    for n in range(0,20):
        test = SVC(gamma=n).fit(X_train, y_train)
        scores.append(round(test.score(X_test, y_test),2))
    gamma = scores.index(max(scores))
    svc = SVC(gamma=gamma)
    # Fit model, predict and cross eval 
    clf = svc.fit(X, y) # Fit the model 
    svc_model = pickle.dumps(clf) # variable containing model object 
    
    # Create dictionary of accuracy measures
    pred_svc = clf.predict(X)
    scores = cross_val_score(svc, X, y, cv=5)
    svc_dict = {"Accuracy Classification Score": metrics.accuracy_score(y, pred_svc), "Precision Score": metrics.precision_score(y, pred_svc, average="macro"), "Recall Score": metrics.recall_score(y, pred_svc, average="macro"), "F-score": metrics.f1_score(y, pred_svc, average="macro"), "Cross Val. Accuracy (+/- %0.2f)" % (scores.std() * 2): scores.mean()}
    # Commit to database
    SVC_results = Results(model_type="Support Vector Machines", model=svc_model, accuracy=str(svc_dict)) 
    db.session.add(SVC_results)
    db.session.commit()

if __name__ == "__main__":
    analysis()