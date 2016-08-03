'''
http://stackoverflow.com/questions/16947276/flask-sqlalchemy-iterate-column-values-on-a-single-row
http://stackoverflow.com/questions/270879/efficiently-updating-database-using-sqlalchemy-orm
http://docs.sqlalchemy.org/en/latest/orm/session_basics.html
'''

from data.extract_log_data import *
from project import db # import database object
from project.models import *
import sqlalchemy


def update_db(df, table):
    # insert dataframe into db line by line
    for i, row in df.iterrows():
        logs = table(room=row["room"], date=row["date"], time=row["time"],
                     associated_client_count=row["associated_client_count"],
                     authenticated_client_count=row["authenticated_client_count"],
                     module_code=None, occupancy=None)
        db.session.add(logs)

        try:
            db.session.commit()
            print("row inserted @", row["room"], row["date"], row["time"], "\n")
        except sqlalchemy.exc.IntegrityError:
            # remove staged changes which cause error
            db.session.rollback()
            print("integrity error @", row["room"], row["date"], row["time"], "\ntrying to update db...")

            # get row which causes integrity constraint
            db_row = db.session.query(table).filter_by(date=row["date"], time=row["time"], room=row["room"]).first()

            # convert the sqlalchemy object and pandas row to dictionaries so they can be merged
            dict_db_row = dict((column, getattr(db_row, column)) for column in db_row.__table__.columns.keys())
            dict_row = dict((column, row[column]) for column in df.columns)

            # overwrite values in dict_row with values already in dict_db_row
            # in other words, only add values from row that are not already in the db
            merged = dict(list(dict_row.items()) + list(dict_db_row.items()))

            # merged["occupancy"] = 9000

            # if the merge doesn't have any new values, don't bother commiting to the db
            if merged == dict_db_row:
                print("no new values to commit @", row["room"], row["date"], row["time"], "\n")
                continue

            # update sqlalchemy object to be committed
            for column in merged:
                setattr(db_row, column, merged[column])

            # this can't fail integrity because it is updating a row already in the db
            db.session.commit()
            print("db updated @", row["room"], row["date"], row["time"], "\n")
            continue

if __name__ == "__main__":
    update_db(log_df("./data/temp_csv/"), Occupy)
