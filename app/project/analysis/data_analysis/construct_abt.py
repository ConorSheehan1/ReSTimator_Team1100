import pandas as pd
import numpy as np
from datetime import datetime
from project.models import Occupy, Module, Location
from project import db

def occupy_df():
	'''Input: database connection

	Output: occupy dataframe
	'''
	# Set up occupy table (Part 1)
	query_occ_1 = db.session.query(Occupy.room, Occupy.date, Occupy.time, Occupy.associated_client_count, Occupy.authenticated_client_count)
	c = query_occ_1.statement.compile(query_occ_1.session.bind)
	df_occupy_1 = pd.read_sql(c.string, query_occ_1.session.bind, params=c.params)
	# Condition 1: time between 9:00 and 17:00
	df_occupy_1["condition1"] = df_occupy_1["time"].apply(lambda x: "true" if 16 >= int(x[0:2]) >= 9 else "false")
	df_occupy_1 = df_occupy_1[df_occupy_1["condition1"] == "true"]
	# Condition 2: quarter past the hour <= time <= quarter past the hour
	df_occupy_1["condition2"] = df_occupy_1["time"].apply(lambda x: "true" if 45 >= int(x[-2:]) >= 15 else "false")
	df_occupy_1 = df_occupy_1[df_occupy_1["condition2"] == "true"]
	# Reformat time (exclude minutes)
	df_occupy_1["time"] = df_occupy_1["time"].apply(lambda x: x[0:3] + "00")
	# Delete condition columns
	del df_occupy_1["condition1"]
	del df_occupy_1["condition2"]

	# Set up occupy table (Part 2)
	query_occ_2 = db.session.query(Occupy.room, Occupy.date, Occupy.time, Occupy.module_code, Occupy.occupancy)
	c = query_occ_2.statement.compile(query_occ_2.session.bind)
	df_occupy_2 = pd.read_sql(c.string, query_occ_2.session.bind, params=c.params)

	# Merge occupy tables
	df_occupy_merge = pd.merge(left = df_occupy_1, right = df_occupy_2, how="outer", on=["room", "date", "time"])

	# Clean dataframe 
	df_occupy = df_occupy_merge.groupby(["room", "date", "time", "module_code"], as_index=False).mean() # df with average auth / assoc client counts
	df_occupy = df_occupy.dropna() # drop rows without both client count and ground truth

	return df_occupy

def module_df():
	'''Input: database connection

	Output: module dataframe
	'''
	query_mod = db.session.query(Module)
	c = query_mod.statement.compile(query_mod.session.bind)
	df_module = pd.read_sql(c.string, query_mod.session.bind, params=c.params)
	return df_module

# def location_df(conn):
def location_df():
	'''Input: database connection

	Output: location dataframe
	'''
	# df_location = pd.read_sql(sql="SELECT * FROM location", con=conn)
	query_loc = db.session.query(Location)
	c = query_loc.statement.compile(query_loc.session.bind)
	df_location = pd.read_sql(c.string, query_loc.session.bind, params=c.params)
	return df_location

def get_day(date_string):
    """Takes date in format yyyy-mm-dd and returns weekday string."""
    year = date_string[:4] 
    month = date_string[5:7]
    day = date_string[8:] 
    return datetime.strptime(year + "," + month + "," + day, "%Y,%m,%d").strftime('%A')

def normalize(df, feature):
    '''Normalize data'''
    return (df[feature] - df[feature].mean()) / df[feature].std()

def removeOutliers(df, feature):
    '''Remove outliers (more than 3 std devs from mean)'''
    return df[np.abs(df[feature] - df[feature].mean()) <= (3 * df[feature].std())]

def convert_perc_int(df):
    ''''''
    df["occupancy"] = df["occupancy"].apply(lambda x: x * 100)
    df["occupancy"] = df["occupancy"].astype(int)
    return df

def adjustment(df):
	''''''
	# Adjustment: Based on assumption of max devices = max of % range * capacity * 2 (see Data_Ana_Final.ipynb for full explanation)
	df["max_devices"] = ((df["occupancy_number"] + (df["capacity"] * .125)) * 2) 
	df["difference"] = df["authenticated_client_count"] - df["max_devices"]
	return df[df["difference"] < 0]

def abt(normal=True, convert=False, adjust=True):
	'''Construct ABT'''
	# create dfs
	df_occupy = occupy_df() 
	df_module = module_df()
	df_location = location_df()
	# merge dfs and drop N/A rows
	df_abt = pd.merge(left = df_occupy, right = df_module, how="outer", on=["module_code"]) 
	df_abt = pd.merge(left = df_abt, right = df_location, how="outer", on=["room"]) 
	df_abt = df_abt.dropna() 
	# Remove rows without registered students i.e. no class
	df_abt = df_abt[df_abt["reg_students"] != 0] 
	# Add occupancy ground truth number to ABT (Capacity * GT%)
	df_abt["occupancy_number"] = df_abt["occupancy"] * df_abt["capacity"] 
	# Remove those rows outside an acceptable error range
	df_abt["Difference"] = df_abt["occupancy_number"] - df_abt["reg_students"]
	df_abt["max_error"] = df_abt["capacity"].apply(lambda x: x * .125)
	df_abt = df_abt[df_abt["Difference"] <= df_abt["max_error"]]
	# Take min between occupancy gt and reg students to remove error in gt measurement
	df_abt["min_occ_reg"] = df_abt.loc[:, ['occupancy_number', 'reg_students']].min(axis=1) 
	if adjust:
		df_abt = adjustment(df_abt)

	df_abt["day"] = df_abt["date"].apply(lambda x: get_day(x)) # Insert day

	if normal:
		df_abt["min_occ_reg_NORM"] = normalize(df_abt, "min_occ_reg")
		df_abt = removeOutliers(df_abt, "min_occ_reg_NORM")
		df_abt["auth_client_count_NORM"] = normalize(df_abt, "authenticated_client_count")
		df_abt = removeOutliers(df_abt, "auth_client_count_NORM")
		del df_abt["min_occ_reg_NORM"] 
		del df_abt["auth_client_count_NORM"] 

	if convert:
		df_abt = convert_perc_int(df_abt)

	return df_abt

def lin_exp_var(df):
	''''''
	return df["authenticated_client_count"].reshape(len(df["authenticated_client_count"]), 1)

def log_exp_var(df):
	''''''
	EXP = []
	for a, o in zip(df["authenticated_client_count"], df['capacity']):
		EXP.append([a, o])
	return np.array(EXP)

def gnb_exp_var(df):
	''''''
	EXP = []
	for a, o in zip(df["authenticated_client_count"] / df["capacity"], df['reg_students']):
		EXP.append([a, o])
	return np.array(EXP)

def knn_exp_var(df):
	''''''
	EXP = []
	for a, o in zip(df["authenticated_client_count"] / df["capacity"], df['reg_students']):
		EXP.append([a, o])
	return np.array(EXP)

def svm_exp_var(df):
	''''''    
	EXP = []
	for a, o in zip(df["authenticated_client_count"], df['capacity']):
		EXP.append([a, o])
	return np.array(EXP)