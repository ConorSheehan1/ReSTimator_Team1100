from project import db # import database object
from project.models import *

# create database and tables
db.create_all() # initializes db based on the schema in the tables.py file

# User Table Testing
user1 = Users(username="admin@ucd.ie", password="admin", confirmed=True, role='admin')
user2 = Users(username="lecturer@ucd.ie", password="lecturer", confirmed=True)

db.session.add(user1)
db.session.add(user2)
db.session.commit()