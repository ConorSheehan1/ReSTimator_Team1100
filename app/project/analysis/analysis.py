from data_analysis import *
import pandas as pd
import sqlite3
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.cross_validation import train_test_split
from sklearn import metrics

conn = sqlite3.connect("../sample.db") # db connection
df_regression = abt(conn).copy() # Construct ABT for linear regression
# conn.close() # close db connection

# Simple linear regression model
X = df_regression["authenticated_client_count"].reshape(len(df_regression["authenticated_client_count"]), 1) # independent variable
y = df_regression["min_occ_reg"] # dependent variable
lm = LinearRegression(fit_intercept=False) # create linear regression object
lm.fit(X, y) # fit the model 
df_regression["predicted_occupancy"] = pd.Series(lm.predict(X), index=df_regression.index) # add predictions to df
df_regression = df_regression[["room", "date", "time", "module_code", "day", "associated_client_count",
							   "authenticated_client_count", "occupancy", "reg_students", "campus", "building",
							   "capacity", "predicted_occupancy"]]

try:
	df_regression.to_sql(name="results", flavor="sqlite", con=conn, if_exists="append", index=False)
except sqlite3.IntegrityError:
	print("Constraint Error: occupy table")
except sqlite3.OperationalError:
	print("Unable to open database or table doesn't contain column")

conn.close()