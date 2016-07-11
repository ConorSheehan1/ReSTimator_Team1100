import sqlite3
import pandas as pd
try:
    from data_analytics.clean_csvs import importer
    from data_analytics.db_config import populate_db
    from data_analytics.predict import get_average
except ImportError:
    from clean_csvs import importer
    from db_config import populate_db
    from predict import get_average


def test_num_rows():
    conn = sqlite3.connect(r"../data/Ucd_Occupancy.db")
    cursor = conn.cursor()
    count = "SELECT COUNT(*) FROM occupy"
    cursor.execute(count)
    # fetch_all returns a tuple in a list, so use [0][0] to get just integer
    # number of rows in database
    num_rows_db = cursor.fetchall()[0][0]

    b02 = importer("../data/CSI WiFiLogs/B-02/")[0]
    b03 = importer("../data/CSI WiFiLogs/B-03/")[0]
    b04 = importer("../data/CSI WiFiLogs/B-04/")[0]

    # merge dataframes together
    all_rooms = pd.concat([b02, b03, b04])

    # get one value per hour
    all_rooms = get_average(all_rooms)

    # number of rows in dataframe
    num_rows_df = len(all_rooms)

    print(num_rows_db, num_rows_df)

    # database is built using outer merge, so no records from wifi logs should be lost
    assert num_rows_db >= num_rows_df


def test_date_time_format():
    # read db
    conn = sqlite3.connect(r"../data/Ucd_Occupancy.db")
    cursor = conn.cursor()
    date_time = "SELECT time, date FROM occupy"
    cursor.execute(date_time)
    date_time_list = cursor.fetchall()

    for tuple in date_time_list:
        time = tuple[0]
        date = tuple[1]

        # time must always be hh:mm with leading zeros
        for value in time.split(":"):
            if len(value) != 2:
                assert False

        # date is always yyyymmdd
        # this test will break in the year 10000, sorry guys no future proofing
        if len(str(date)) != 8:
            assert False
    # if all cases don't assert false, assert true
    assert True

if __name__ == "__main__":
    test_num_rows()
    test_date_time_format()