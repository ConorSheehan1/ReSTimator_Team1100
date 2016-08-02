import sqlite3
from data.extract_log_data import *
# from project import db # import database object
from project.models import *
import sqlalchemy

if __name__ == "__main__":

    # conn = sqlite3.connect("./project/test.db")
    # cur = conn.cursor()
    logs = log_df("./data/temp_csv/")
    # print(logs)

    for tup in logs.itertuples():
        logs = Occupy(room=tup[1], date=int(tup[2]), time=tup[3], associated_client_count=int(tup[4]),
                      authenticated_client_count=int(tup[5]), module_code=None, occupancy=None)
        db.session.add(logs)
        try:
            db.session.commit()

        # except sqlite3.IntegrityError:
        except sqlalchemy.exc.IntegrityError:
            print("integrity error")
            # logs = Occupy(room=tup[1], date=tup[2], time=tup[3], associated_client_count=tup[4],
            #               authenticated_client_count=tup[5], module_code=None, occupancy=None)
            # db.session.update(logs)




    #     sql = 'update table set column = %s where column = %s'
    #     cur.execute(sql, (tup['whatver'], tup['something']))
    # conn.commit()






# # sqlalchemy
# print(db)
#
# # don't know how to tup df into db efficiently (have to use name of every column?
