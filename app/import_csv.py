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

        try:
            db.session.commit()

        # if commiting to db fails, get row which causes integrity constraint
        except sqlalchemy.exc.IntegrityError:

            # remove staged changes which cause error
            db.session.rollback()
            print("integrity error @", row["room"], row["date"], row["time"])
            print("trying to update db ...")
            # get row which causes integrity constraint
            db_row = Occupy.query.filter_by(date=row["date"], time=row["time"], room=row["room"]).first()

            # convert the sqlalchemy object and pandas row to dictionaries so they can be merged
            dict_db_row = dict((column, getattr(db_row, column)) for column in db_row.__table__.columns.keys())
            dict_row = dict((column, row[column]) for column in df.columns)

            # test that rows are updated correctly
            dict_row["room"] = "B5000"
            print(dict_db_row, "\n", dict_row)

            # overwrite values in dict_row with values already in dict_db_row
            # in other words, only add values from row that are not already in the db
            merged = dict(list(dict_row.items()) + list(dict_db_row.items()))
            print(merged)

            updated = logs(room=merged["room"], date=merged["date"], time=merged["time"],
                           associated_client_count=merged["associated_client_count"],
                           authenticated_client_count=merged["authenticated_client_count"],
                           module_code=merged["module_code"], occupancy=merged["occupancy"])

            db.session.add(updated)

            try:
                db.session.commit()
            except sqlalchemy.exc.IntegrityError:
                print("data already in db", dict_row)
                db.session.rollback()
                continue

            continue


            # df_copy = row.copy(deep=True)
            # print(df_copy)

            # df_db = pd.DataFrame(columns=logs.columns, data=db_row.values)

            # print(db_row.time)
            # values = [val for val in dir(db_row) if val in df.columns]
            # print(values)