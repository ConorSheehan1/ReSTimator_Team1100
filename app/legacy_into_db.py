from data import *
import sqlite3
# from app.update_db import update_db
# from project.models import *
# from data.extract_legacy import *
# from project import db


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
		print("gt:", df_gt["date"])
		df_gt["time"] = df_gt["time"].apply(lambda x: x.strftime("%H:%M")) # format time

		# Extract log data from csvs
		extract_csvs(path_logs)
		df_logs = log_df(path_logs)
		print("logs:", df_logs["date"])

		# Combine dfs
		df_merge = pd.merge(left=df_gt, right=df_logs, how="outer", on=["room", "date", "time"])
		populate_db(df_merge, "occupy", path_db)
		delete_csvs(path_logs)
	except sqlite3.IntegrityError:
		print("Constraint Error: occupy table")
	except sqlite3.OperationalError:
		print("Unable to open database")
	except KeyError:
		print("No zip file in directory (or format of csvs has changed)")
		
if __name__ == "__main__":
	legacy()