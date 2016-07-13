'''
Notes:
This script needs to be updated to allow for parts of a dataframe to be input into the database

References:
http://stackoverflow.com/questions/4960048/python-3-and-mysql
http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.to_sql.html
http://stackoverflow.com/questions/734689/sqlite-primary-key-on-multiple-columns

Fix import errors
http://stackoverflow.com/questions/16981921/relative-imports-in-python-3

Update:
https://docs.python.org/2/library/sqlite3.html
check total_changes for testing to see how many new rows were created!
use append not replace
split day into table or use python datetime.datetime(year, month, date).weekday()

SQLITE case sensitive using double quotes
http://sqlite.1065341.n5.nabble.com/Case-sensitive-table-names-td2818.html
SQLITE date?
http://stackoverflow.com/questions/29749356/python-pandas-export-structure-only-no-rows-of-a-dataframe-to-sql/
'''


import sqlite3
import pandas as pd
try:
    from data_analytics import clean_csvs
    from data_analytics import clean_ground_truth
    from data_analytics import clean_timetable
    from data_analytics import predict
except ImportError:
    import clean_csvs
    import clean_ground_truth
    import clean_timetable
    import predict


def create_tables():
    conn = sqlite3.connect(r"./data/ucd_occupancy.db")
    cursor = conn.cursor()

    prefix = "CREATE TABLE IF NOT EXISTS "

    occupy = prefix + "occupy (room VARCHAR, date INT, time VARCHAR, occupancy REAL, module_code VARCHAR, " \
                      "associated_client_count INT, authenticated_client_count INT," \
                      "PRIMARY KEY (time, date, room));"
    cursor.execute(occupy)

    location_table = prefix + "location (room VARCHAR, building VARCHAR, campus VARCHAR, capacity INT, " \
                              "PRIMARY KEY(room, building, campus)" \
                              "FOREIGN KEY(room) REFERENCES occupy(room));"
    cursor.execute(location_table)

    module_table = prefix + "module (module_code VARCHAR, reg_students INT, " \
                            "PRIMARY KEY (module_code)" \
                            "FOREIGN KEY(module_code) REFERENCES occupy(module_code));"
    cursor.execute(module_table)
    conn.close()


def populate_db(list_of_room_codes, method="append", do_print=False):
    conn = sqlite3.connect(r"./data/ucd_occupancy.db")

    # get all csv dataframes
    iter_csvs = clean_csvs.concat_log_dfs(list_of_room_codes, do_print)
    df_logs = iter_csvs[0]

    iter_gt = clean_ground_truth.import_ground_truth("./data/CSI Occupancy report.xlsx", do_print)
    df_location = iter_gt[1]
    # use inner merge for rooms, only want common locations to have full location data
    df_full_location = pd.merge(df_location, iter_csvs[1], how="inner", on="room")
    df_full_location.to_sql(name='location', flavor='sqlite', con=conn, index=False,  if_exists=method)

    df_timetable = clean_timetable.fix_merged_cells("./data/", "B0.02 B0.03 B0.04 Timetable.xlsx", do_print)

    df_module = df_timetable[["module_code", "reg_students"]].copy()
    # drop duplicated module codes, fix?
    df_module.drop_duplicates(subset=["module_code"], inplace=True)
    df_module.to_sql(name='module', flavor='sqlite', con=conn, index=False,  if_exists=method)

    df_ground_truth = iter_gt[0]
    # use outer merge for ground truth, keep occupancy data even if timetable data doesn't match and vice versa
    df_occupy = pd.merge(df_ground_truth, df_timetable, how="outer", on=["time", "date", "room"])
    df_occupy = pd.merge(df_occupy, df_logs, how="outer", on=["time", "date", "room"])

    # outer merge can result in duplicates
    df_occupy.drop_duplicates(inplace=True)
    # convert floats from merge back to ints
    df_occupy["date"] = df_occupy["date"].astype(int)
    df_occupy.drop("reg_students", axis=1, inplace=True)
    df_occupy.to_sql(name='occupy', flavor='sqlite', con=conn, index=False,  if_exists=method)

    conn.close()

    return df_occupy

if __name__ == "__main__":
    '''
    for testing use replace
    change to update for actual use
    '''
    create_tables()
    populate_db(["B-02", "B-03", "B-04"], "replace", True)
    # populate_db(["B-02", "B-03", "B-04"])
