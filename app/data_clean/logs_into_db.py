from extract_log_data.extract_log_data import *
import sqlite3

def populate_db(df, table_name, db_path):
	'''Connect to database and append data to table'''
	conn = sqlite3.connect(db_path)
	df.to_sql(name=table_name, flavor="sqlite", con=conn, if_exists="append", index=False)
	conn.close()

if __name__ == "__main__":
	try:
		extract_csvs("./log_data")
		df = log_df()
		populate_db(df, "occupy", "../../app/project/sample.db")
		delete_zips()
		delete_csvs()
	except sqlite3.IntegrityError:
		print("Constraint Error")
		delete_zips()
		delete_csvs()