from data.extract_log_data import *
from project import db # import database object

if __name__ == "__main__":
    logs = log_df("./data/temp_csv/")
    print(logs)
    print(db)


# print(db)
# db.session.add(user)
# db.session.commit()