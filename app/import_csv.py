'''
http://stackoverflow.com/questions/16947276/flask-sqlalchemy-iterate-column-values-on-a-single-row
'''

from data.extract_log_data import *
from project import db # import database object
from project.models import *
import sqlalchemy
import pandas as pd

if __name__ == "__main__":

    # conn = sqlite3.connect("./project/test.db")
    # cur = conn.cursor()
    df = log_df("./data/temp_csv/")
    # print(logs)

    # insert dataframe into db line by line
    for i, row in df.iterrows():

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

            # df_db = pd.DataFrame(columns=logs.columns, data=db_row.values)

            # print(db_row.time)
            # values = [val for val in dir(db_row) if val in df.columns]
            # print(values)

            db_row_dict = dict((col, getattr(db_row, col)) for col in db_row.__table__.columns.keys())
            print(db_row_dict)

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