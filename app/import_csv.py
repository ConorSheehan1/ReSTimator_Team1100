'''
http://stackoverflow.com/questions/16947276/flask-sqlalchemy-iterate-column-values-on-a-single-row
http://stackoverflow.com/questions/270879/efficiently-updating-database-using-sqlalchemy-orm
'''

from data.extract_log_data import *
from project import db # import database object
from project.models import *
import sqlalchemy


def update_db(df):
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
            # db_row = Occupy.query.filter_by(date=row["date"], time=row["time"], room=row["room"]).first()
            db_row = db.session.query(Occupy).filter_by(date=row["date"], time=row["time"], room=row["room"]).first()

            # convert the sqlalchemy object and pandas row to dictionaries so they can be merged
            dict_db_row = dict((column, getattr(db_row, column)) for column in db_row.__table__.columns.keys())
            dict_row = dict((column, row[column]) for column in df.columns)

            # overwrite values in dict_row with values already in dict_db_row
            # in other words, only add values from row that are not already in the db
            merged = dict(list(dict_row.items()) + list(dict_db_row.items()))
            print(merged)
            merged["module_code"] = "asdf"

            db_row.module_code = merged["module_code"]

            try:
                db.session.commit()
                print("db updated")
            except sqlalchemy.exc.IntegrityError:
                print("data already in db", dict_row)
                db.session.rollback()
                continue
            continue

if __name__ == "__main__":
    update_db(log_df("./data/temp_csv/"))