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
    # get list of primary key(s)
    pk_list = [key.name for key in sqlalchemy.inspect(table).primary_key]
    print(pk_list)

    # insert dataframe into db line by line
    for i, row in df.iterrows():
        # get all values from df and put in dictionary
        existing_args = {column: row[column] for column in df.columns}

        # get all values required to construct table and put in dictionary
        empty_args = {column: None for column in table.__table__.columns.keys()}

        # merge two dicts, overwrite empty_args with existing_args
        kwargs = dict(list(empty_args.items()) + list(existing_args.items()))
        data = table(**kwargs)
        db.session.add(data)

        try:
            db.session.commit()
            print("row inserted @", end="")
            for value in pk_list:
                print("", row[value], end="")
            print("\n")
        except sqlalchemy.exc.IntegrityError:
            # remove staged changes which caused integrity error
            db.session.rollback()

            print("integrity error @", end="")
            for value in pk_list:
                print("", row[value], end="")
            print("\ntrying to update db...")

            # create dictionary of primary key values which caused integrity error
            primary_key_kwargs = dict((value, row[value]) for value in pk_list)

            # get row which causes integrity error
            db_row = db.session.query(table).filter_by(**primary_key_kwargs).first()

            # convert the sqlalchemy object to a dictionary so it can be merged with row dictionary (existing_args)
            dict_db_row = dict((column, getattr(db_row, column)) for column in db_row.__table__.columns.keys())

            # test to see that function does update rows
            # existing_args["occupancy"] = None
            # existing_args["occupancy"] = 9000

            # overwrite values in dict_db_row with existing_args
            # in other words, overwrite any data in the db with new data provided at the row which cause integrity error
            merged = dict(list(dict_db_row.items()) + list(existing_args.items()))

            # if the merge doesn't have any new values, don't bother committing to the db
            if merged == dict_db_row:
                print("no new values to commit @", row["room"], row["date"], row["time"], "\n")
                continue

            # update attributes of sqlalchemy object to be committed
            for column in merged:
                setattr(db_row, column, merged[column])

            # this can't fail integrity because it is updating a row already in the db
            db.session.commit()
            print("db updated @", row["room"], row["date"], row["time"], "\n")
            continue

if __name__ == "__main__":
    update_db(log_df("./data/temp_csv/"), Occupy)
