import sqlite3
import pandas as pd
try:
    from data_analytics.clean_csvs import importer
except ImportError:
    from clean_csvs import importer


def test_num_rows():
    conn = sqlite3.connect(r"../data/Ucd_Occupancy.db")
    cursor = conn.cursor()
    count = "SELECT COUNT(*) FROM wifi_logs"
    cursor.execute(count)
    # fetch_all returns a tuple in a list, so use [0][0] to get just integer
    # number of rows in database
    num_rows_db = cursor.fetchall()[0][0]

    b02 = importer("../data/CSI WiFiLogs/B-02/")[0]
    b03 = importer("../data/CSI WiFiLogs/B-03/")[0]
    b04 = importer("../data/CSI WiFiLogs/B-04/")[0]
    all_rooms = pd.concat([b02, b03, b04])

    # number of rows in dataframe
    num_rows_df = len(all_rooms)

    print(num_rows_df, num_rows_db)
    assert num_rows_db == num_rows_df

if __name__ == "__main__":
    test_num_rows()