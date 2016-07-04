'''
Notes:
This script needs to be updated to allow for parts of a dataframe to be input into the database

References:
http://stackoverflow.com/questions/4960048/python-3-and-mysql
http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.to_sql.html
http://stackoverflow.com/questions/734689/sqlite-primary-key-on-multiple-columns

Fix import errors
http://stackoverflow.com/questions/16981921/relative-imports-in-python-3
'''


import sqlite3
try:
    from data_analytics import clean_csvs
    from data_analytics import clean_ground_truth
except ImportError:
    import clean_csvs
    import clean_ground_truth


def create_tables():
    conn = sqlite3.connect(r"./data/Ucd_Occupancy.db")
    cursor = conn.cursor()
    # create table
    logs_table = "CREATE TABLE IF NOT EXISTS WiFiLogs " \
                 "(Key VARCHAR, Event_Time VARCHAR, Associated_Client_Count INT, " \
                 "Authenticated_Client_Count INT, PRIMARY KEY (Key, Event_Time));"
    cursor.execute(logs_table)

    location_table = "CREATE TABLE IF NOT EXISTS Location (Room VARCHAR, Capacity VARCHAR, PRIMARY KEY(Room));"
    cursor.execute(location_table)

    conn.close()


def populate_db(list_of_room_codes):
    # create database and tables
    conn = sqlite3.connect(r"./data/Ucd_Occupancy.db")

    # convert csv to dataframe, and import dataframe to database
    for code in list_of_room_codes:
        df_logs = clean_csvs.importer("./data/CSI WiFiLogs/" + code + "/")[0]
        df_logs.to_sql(name='WiFiLogs', flavor='sqlite', con=conn, index=False,  if_exists='append')

    df_location = clean_ground_truth.import_ground_truth("./data/CSI Occupancy report.xlsx")[1]
    df_location.to_sql(name='Location', flavor='sqlite', con=conn, index=False,  if_exists='append')

    conn.close()


    # print("print", clean_ground_truth.import_ground_truth("./data/CSI Occupancy report.xlsx")[1])


if __name__ == "__main__":
    create_tables()
    populate_db(["B-02", "B-03", "B-04"])

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~ Old stuff using mysql instead of sqlite ~~~~
# import pymysql as MS
#
# db1 = MS.connect(host="localhost", user="root", passwd="")
# cursor = db1.cursor()
# sql = 'CREATE DATABASE Ucd_Occupancy'
# cursor.execute(sql)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
