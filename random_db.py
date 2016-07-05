from app import db, tables



u = tables.Results(day = "Mon", time = "222222", module = "COMP4", estimate = 50)
db.session.add(u)

t = tables.Results(day = "Tue", time = "322332", module = "COMP3", estimate = 60)
db.session.add(t)

v = tables.Results(day = "Fri", time = "221112", module = "COMP2", estimate = 70)
db.session.add(v)
db.session.commit()


