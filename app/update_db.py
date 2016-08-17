'''
http://stackoverflow.com/questions/16947276/flask-sqlalchemy-iterate-column-values-on-a-single-row
http://stackoverflow.com/questions/270879/efficiently-updating-database-using-sqlalchemy-orm
http://docs.sqlalchemy.org/en/latest/orm/session_basics.html
'''

# from data.extract_log_data import *
# from data.extract_legacy import *
# from project import db # import database object
# from project.models import *
import sqlalchemy
from flask import flash


def update_db(db, df, table, gt=False):
    """
    Updates the database with user data.
    
    gt is whether or not the user is inputting a single row of ground truth data
    """
    
    # get list of primary key(s)
    pk_list = [key.name for key in sqlalchemy.inspect(table).primary_key]
    print("primary keys:", pk_list, "\n")

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
            if gt:
                flash("Thank you. Your data has been recorded.")
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
            # print(dict_db_row)

            # test to see that function does update rows
            # existing_args["occupancy"] = None
            # existing_args["occupancy"] = 9000

            # overwrite values in dict_db_row with existing_args
            # in other words, overwrite any data in the db with new data provided at the row which cause integrity error
            merged = dict(list(dict_db_row.items()) + list(existing_args.items()))

            # if the merge doesn't have any new values, don't bother committing to the db
            if merged == dict_db_row:
                print("no new values to commit @", end="")
                for value in pk_list:
                    print("", row[value], end="")
                print("\n")
                if gt:
                    flash("Your data has already been recorded. Please check that you selected the correct information.")
                continue

            # update attributes of sqlalchemy object to be committed
            for column in merged:
                setattr(db_row, column, merged[column])

            # this can't fail integrity because it is updating a row already in the db
            db.session.commit()

            print("db updated @", end="")
            for value in pk_list:
                print("", row[value], end="")
            print("\n")
            if gt:
                flash("Thank you. Your data has been recorded.")

if __name__ == "__main__":
    # # --WIFI LOGS---
    # print(log_df("./data/temp_csv/"))
    # update_db(log_df("./data/temp_csv/"), Occupy)

    # # ----LOCATION---
    # # write new values in dictionary and merge into existing location dataframe.
    # # check if db is update correctly
    # data = {'0': {'campus': "Belfield", 'building': "Computer Science", 'room': "B-004", 'capacity': 100000},
    #         '1': {'campus': "test", 'building': "test", 'room': "test", 'capacity': 110000}}
    # df_test_data = pd.DataFrame(data)
    # df_test_data = df_test_data.T

    # get location data
    df_location = extract("./data/legacy_data/legacy_data.xlsx", "location")
    # # merge with test data
    # df_location = pd.merge(df_test_data, df_location, how="outer")

    print(df_location)
    update_db(df_location, Location)
