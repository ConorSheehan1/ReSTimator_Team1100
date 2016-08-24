from project import db # import database object
from project.models import *
from data import *
import sqlite3
from analysis import analysis


def legacy():
	try:
		df_mod = extract(path_legacy_xl, "modules")
		populate_db(df_mod, "module", path_db)
	except sqlite3.IntegrityError:
		print("Constraint Error: modules table")

	try:
		df_loc = extract(path_legacy_xl, "location")
		populate_db(df_loc, "location", path_db)
	except sqlite3.IntegrityError:
		print("Constraint Error: location table")	

	try:	
		# Extract ground truth
		df_gt = extract(path_legacy_xl, "ground_truth")
		df_gt["date"] = df_gt["date"].apply(lambda x: str(x)[:10])
		df_gt["time"] = df_gt["time"].apply(lambda x: x.strftime("%H:%M")) # format time

		# Extract log data from csvs
		extract_csvs(path_logs)
		df_logs = log_df(path_logs)

		# Combine dfs
		df_merge = pd.merge(left=df_gt, right=df_logs, how="outer", on=["room", "date", "time"])
		populate_db(df_merge, "occupy", path_db)
		delete_all(path_logs)
	except sqlite3.IntegrityError:
		print("Constraint Error: occupy table")
	except sqlite3.OperationalError:
		print("Unable to open database")
	except KeyError:
		print("No zip file in directory (or format of csvs has changed)")

# create database and tables
db.create_all() # initializes db based on the schema in the tables.py file

# User Table Testing
user1 = Users(username="admin@ucd.ie", password="admin", confirmed=True, role='admin')
user2 = Users(username="lecturer@ucd.ie", password="lecturer", confirmed=True)

db.session.add(user1)
db.session.add(user2)
db.session.commit()

# Set up db with legacy data
legacy()

# Populate db with analysis results
analysis()