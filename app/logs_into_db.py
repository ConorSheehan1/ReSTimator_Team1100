from data import *
import sqlite3

# NEED TO FIND WAY TO UPDATE TABLE FOR NEW LOGS

if __name__ == "__main__":
	# path = "./data/log_data"
	# path_db = "./project/sample.db"

	try:
		extract_csvs(path_logs)
		df = log_df()
		os.chdir(path_cd)
		populate_db(df, "occupy", path_db)
		os.chdir(path_logs)
		delete_zips()
		delete_csvs()
	except sqlite3.IntegrityError:
		print("Constraint Error")
		delete_zips()
		delete_csvs()