from extract_legacy.clean_legacy import extract_legacy
from extract_log_data.extract_log_data import *
import sqlite3

def populate_db(df, table_name, db_path):
	'''Connect to database and append data to table'''
	conn = sqlite3.connect(db_path)
	df.to_sql(name=table_name, flavor="sqlite", con=conn, if_exists="append", index=False)
	conn.close()

if __name__ == "__main__":
	path = "./legacy_data/legacy_data.xlsx"

	try:
		df_mod = extract_legacy(path, "modules")
		populate_db(df_mod, "module", "../app/project/sample.db")
	except sqlite3.IntegrityError:
		print("Constraint Error: modules table")

	try:
		df_loc = extract_legacy(path, "location")
		populate_db(df_loc, "location", "../app/project/sample.db")
	except sqlite3.IntegrityError:
		print("Constraint Error: location table")	

	try:	
		df_gt = extract_legacy(path, "ground_truth")
		df_gt["time"] = df_gt["time"].apply(lambda x: x.strftime("%H:%M")) # format time	

		extract_csvs("./log_data")
		df_logs = log_df()

		df_merge = pd.merge(left = df_gt, right = df_logs, how="outer", on=["room", "date", "time"]) 
		populate_db(df_merge, "occupy", "../../app/project/sample.db")
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