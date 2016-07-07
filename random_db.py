from app import db, tables

# User Table Testing
user1 = tables.Users(username="Andy", password="22222") 
db.session.add(user1)
user2 = tables.Users(username="Stephen", password="22223") 
db.session.add(user2)
user3 = tables.Users(username="Conor", password="22224") 
db.session.add(user3)


# Results Table Testing
# u = tables.Results(day = "Mon", time = "222222", module = "COMP4", estimate = 50)
# db.session.add(u)
# t = tables.Results(day = "Tue", time = "322332", module = "COMP3", estimate = 60)
# db.session.add(t)
# v = tables.Results(day = "Fri", time = "221112", module = "COMP2", estimate = 70)
# db.session.add(v)

db.session.commit()


# SQLAlchemy COMMANDS:

# 1. select * from tablename
# tablename.query.all() 

# 2. insert values
# db.session.add(tablename(values)) 
# db.session.commit()

 