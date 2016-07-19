from project import db
from project.models import *

# User Table Testing
user = Users(username="admin@ucd.ie", password="admin") 
db.session.add(user)

# Results Table Testing
# u = Results(day = "Mon", time = "222222", module = "COMP4", estimate = 50)
# db.session.add(u)
# t = Results(day = "Tue", time = "322332", module = "COMP3", estimate = 60)
# db.session.add(t)
# v = Results(day = "Fri", time = "221112", module = "COMP2", estimate = 80)
# db.session.add(v)
# w = Results(day = "Fri", time = "221113", module = "COMP4", estimate = 70)
# db.session.add(w)

db.session.commit()


# SQLAlchemy COMMANDS:

# 1. select * from tablename
# tablename.query.all() 

# 2. insert values
# db.session.add(tablename(values)) 
# db.session.commit()

# 3. select distinct day from Results order by day
# db.session.query(Results.day).distinct().order_by(Results.day)

# 4. select * from tablename where username = peter
# tablename.query.filter_by(username='peter').all()
# or
# tablename.query.filter(tablename.email.endswith('@example.com')).all()

 