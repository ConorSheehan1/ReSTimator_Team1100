from data import *
import sqlite3


if __name__ == "__main__":
	path_cd = os.path.dirname(os.path.abspath(__file__))

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
		df_gt["time"] = df_gt["time"].apply(lambda x: x.strftime("%H:%M")) # format time	
		# Extract log data from csvs
		extract_csvs(path_logs)
		df_logs = log_df()
		# Combine dfs
		df_merge = pd.merge(left = df_gt, right = df_logs, how="outer", on=["room", "date", "time"]) 
		os.chdir(path_cd)
		populate_db(df_merge, "occupy", path_db)
		os.chdir(path_logs)
		delete_zips()
		delete_csvs()
	except sqlite3.IntegrityError:
		print("Constraint Error: occupy table")
		delete_zips()
		delete_csvs()
	except sqlite3.OperationalError:
		print("Unable to open database")
		delete_zips()
		delete_csvs()
	except KeyError:
		print("No zip file in directory (or format of csvs has changed)")