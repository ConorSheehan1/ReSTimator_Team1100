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

SQLITE case sensitive using double quotes
http://sqlite.1065341.n5.nabble.com/Case-sensitive-table-names-td2818.html
'''


import sqlite3
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

    logs_table = prefix + "wifi_logs (campus VARCHAR, building VARCHAR, room VARCHAR, Event_Time VARCHAR," \
                          " Associated_Client_Count INT, Authenticated_Client_Count INT," \
                          " PRIMARY KEY (campus, building, room, Event_Time));"
    cursor.execute(logs_table)

    location_table = prefix + "location (room VARCHAR, capacity INT, " \
                              "PRIMARY KEY(room));"
    cursor.execute(location_table)

    module_table = prefix + "module (module_code VARCHAR, reg_students INT," \
                            "PRIMARY KEY (module_code));"
    cursor.execute(module_table)

    ground_truth = prefix + "ground_truth (time VARCHAR, occupancy INT, room VARCHAR," \
                            "PRIMARY KEY (time, Room));"
    cursor.execute(ground_truth)
    conn.close()


def populate_db(list_of_room_codes, method="append"):
    conn = sqlite3.connect(r"./data/ucd_occupancy.db")

    # convert csv to dataframe, and import dataframe to database
    for code in list_of_room_codes:
        df_logs = clean_csvs.importer("./data/CSI WiFiLogs/" + code + "/")[0]
        df_logs.to_sql(name='wifi_logs', flavor='sqlite', con=conn, index=False,  if_exists=method)

    iter_gt = clean_ground_truth.import_ground_truth("./data/CSI Occupancy report.xlsx")
    df_location = iter_gt[1]
    df_location.to_sql(name='location', flavor='sqlite', con=conn, index=False,  if_exists=method)

    df_ground_truth = iter_gt[0]
    df_ground_truth.to_sql(name='ground_truth', flavor='sqlite', con=conn, index=False,  if_exists=method)

    df_module = clean_timetable.fix_merged_cells("./data/", "B0.02 B0.03 B0.04 Timetable.xlsx")
    df_module.to_sql(name='module', flavor='sqlite', con=conn, index=False,  if_exists=method)

    conn.close()

    # print("print", clean_ground_truth.import_ground_truth("./data/CSI Occupancy report.xlsx")[1])


if __name__ == "__main__":
    '''
    for testing use replace
    change to update for actual use
    '''
    create_tables()
    populate_db(["B-02", "B-03", "B-04"], "replace")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~ Old stuff using mysql instead of sqlite ~~~~
# import pymysql as MS
#
# db1 = MS.connect(host="localhost", user="root", passwd="")
# cursor = db1.cursor()
# sql = 'CREATE DATABASE Ucd_Occupancy'
# cursor.execute(sql)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
