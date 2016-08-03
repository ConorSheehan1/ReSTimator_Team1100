import sqlite3
from data.extract_log_data import *
from project import db # import database object
from project.models import *
import sqlalchemy
import pandas as pd

if __name__ == "__main__":

    # conn = sqlite3.connect("./project/test.db")
    # cur = conn.cursor()
    logs = log_df("./data/temp_csv/")
    # print(logs)

    # insert dataframe into db line by line
    for i, row in logs.iterrows():

        logs = Occupy(room=row["room"], date=row["date"], time=row["time"],
                      associated_client_count=row["associated_client_count"],
                      authenticated_client_count=row["authenticated_client_count"],
                      module_code=None, occupancy=None)
        db.session.add(logs)

        # if commiting to db fails, get row with integrity constraint and merge, then try to commit
        try:
            db.session.commit()

        # except sqlite3.IntegrityError:
        except sqlalchemy.exc.IntegrityError:
            db.session.rollback()
            print("integrity error", row["time"])
            db_row = Occupy.query.filter_by(date=row["date"], time=row["time"], room=row["room"]).first()

            # df_copy = row.copy(deep=True)
            # print(df_copy)

            print(db_row.date)
            continue





    #     sql = 'update table set column = %s where column = %s'
    #     cur.execute(sql, (tup['whatver'], tup['something']))
    # conn.commit()




'''
    for tup in logs.itertuples():
        logs = Occupy(room=tup[1], date=int(tup[2]), time=tup[3], associated_client_count=int(tup[4]),
                      authenticated_client_count=int(tup[5]), module_code=None, occupancy=None)
        db.session.add(logs)

        # if commiting to db fails, get row with integrity constraint and merge, then try to commit
        try:
            db.session.commit()

        # except sqlite3.IntegrityError:
        except sqlalchemy.exc.IntegrityError:
            print("integrity error")
                '''