from .extract_legacy import *
from .extract_log_data import *

path_legacy_xl = "./data/legacy_data/legacy_data.xlsx"
path_logs = "./data/log_data/"
path_db = "./project/sample.db"


def populate_db(df, table_name, db_path):
	'''Connect to database and append data to table'''
	conn = sqlite3.connect(db_path)
	df.to_sql(name=table_name, flavor="sqlite", con=conn, if_exists="append", index=False)
	conn.close()