import pandas as pd

def occupy_df(conn):
	'''Input: database connection

	Output: occupy dataframe
	'''
	# Set up occupy table (Part 1)
	df_occupy_1 = pd.read_sql(sql="SELECT room, date, time, associated_client_count, authenticated_client_count FROM occupy", con=conn)
	# Condition 1: time between 9:00 and 17:00
	df_occupy_1["condition1"] = df_occupy_1["time"].apply(lambda x: "true" if 17 >= int(x[0:2]) >= 9 else "false")
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
	df_occupy_2 = pd.read_sql(sql="SELECT room, date, time, module_code, occupancy FROM occupy", con=conn)

	# Merge occupy tables
	df_occupy_merge = pd.merge(left = df_occupy_1, right = df_occupy_2, how="outer", on=["room", "date", "time"])

	# Clean dataframe 
	df_occupy = df_occupy_merge.groupby(["room", "date", "time", "module_code"], as_index=False).mean() # df with average auth / assoc client counts
	df_occupy = df_occupy.dropna() # drop rows with NaN

	# close db connection
	return df_occupy

def module_df(conn):
	'''Input: database connection

	Output: module dataframe
	'''
	df_module = pd.read_sql(sql="SELECT * FROM module", con=conn)
	return df_module

def location_df(conn):
	'''Input: database connection

	Output: location dataframe
	'''
	df_location = pd.read_sql(sql="SELECT * FROM location", con=conn)
	return df_location

def abt(conn):
	'''Construct ABT'''
	# create dfs
	df_occupy = occupy_df(conn) 
	df_module = module_df(conn)
	df_location = location_df(conn)
	# merge dfs
	df_abt = pd.merge(left = df_occupy, right = df_module, how="outer", on=["module_code"]) 
	df_abt = pd.merge(left = df_abt, right = df_location, how="outer", on=["room"]) 

	df_abt["occupancy_number"] = df_abt["occupancy"] * df_abt["capacity"] # create occupancy_number column

	# Issue: ground truth says there are more students than what is registered
	df_abt = df_abt[(df_abt["reg_students"] - df_abt["occupancy_number"]) / df_abt["capacity"] >= -0.1] # remove those that have an error larger than 10%

	# Adjust occupancy number within 10% error range (bring occupancy down to the max registered)
	df_abt["reg_students_less_occ"] = df_abt["reg_students"] - df_abt["occupancy_number"]
	df_abt["adjustment"] = df_abt["reg_students_less_occ"].apply(lambda x: x if x <= 0 else 0)
	df_abt["occupancy_number_adj"] = df_abt["adjustment"] + df_abt["occupancy_number"]

	# Need to figure out how to handle 0% gt number but clearly has clients and classes (some are correct though based on client count)

	return df_abt


