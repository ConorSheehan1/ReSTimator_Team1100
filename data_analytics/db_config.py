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
except ImportError:
    import clean_csvs
    import clean_ground_truth
    import clean_timetable


def create_tables():
    conn = sqlite3.connect(r"./data/ucd_occupancy.db")
    cursor = conn.cursor()

    prefix = "CREATE TABLE IF NOT EXISTS "

    logs_table = prefix + "wifi_logs (campus VARCHAR, building VARCHAR, room VARCHAR, event_time VARCHAR," \
                          " associated_client_count INT, authenticated_client_count INT," \
                          " PRIMARY KEY (campus, building, room, event_time));"
    cursor.execute(logs_table)

    location_table = prefix + "location (room VARCHAR, capacity INT, " \
                              "PRIMARY KEY(room));"
    cursor.execute(location_table)

    module_table = prefix + "module (module_code VARCHAR, reg_students INT, " \
                            "PRIMARY KEY (module_code));"
    cursor.execute(module_table)

    # Real is equivilant to float in slqite
    ground_truth = prefix + "ground_truth (time VARCHAR, occupancy REAL, room VARCHAR, date INT, day VARCHAR," \
                            "module_code VARCHAR, reg_students INT," \
                            "PRIMARY KEY (time, room, date));"
    cursor.execute(ground_truth)
    conn.close()


def populate_db(list_of_room_codes, method="append", do_print=False):
    conn = sqlite3.connect(r"./data/ucd_occupancy.db")

    # convert csv to dataframe, and import dataframe to database
    # get all csv dataframes
    iter_csvs = clean_csvs.concat_log_dfs(list_of_room_codes, do_print)
    df_logs = iter_csvs[0]
    df_logs.to_sql(name='wifi_logs', flavor='sqlite', con=conn, index=False,  if_exists=method)

    iter_gt = clean_ground_truth.import_ground_truth("./data/CSI Occupancy report.xlsx", do_print)
    df_location = iter_gt[1]
    df_full_location = pd.merge(df_location, iter_csvs[1], on="room")
    df_full_location.to_sql(name='location', flavor='sqlite', con=conn, index=False,  if_exists=method)

    df_timetable = clean_timetable.fix_merged_cells("./data/", "B0.02 B0.03 B0.04 Timetable.xlsx", do_print)

    df_module = df_timetable[["module_code", "reg_students"]].copy()
    df_module.drop_duplicates(inplace=True)
    df_module.to_sql(name='module', flavor='sqlite', con=conn, index=False,  if_exists=method)

    # merge ground truth with timetable based on date room and time
    df_ground_truth = iter_gt[0]
    print(df_ground_truth, df_timetable)
    df_full_gt = pd.merge(df_ground_truth, df_timetable, how="left", on=["time", "room", "date"])
    print(df_full_gt)
    df_full_gt.to_sql(name='ground_truth', flavor='sqlite', con=conn, index=False,  if_exists=method)

    if do_print:
        print("Data saved to db!")

    # print(df_ground_truth, df_timetable)

    conn.close()

if __name__ == "__main__":
    '''
    for testing use replace
    change to update for actual use
    '''
    create_tables()
    populate_db(["B-02", "B-03", "B-04"], "replace")
