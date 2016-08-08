from project import db
from sqlalchemy import *
from flask_wtf import Form
from wtforms import SelectField
from project.models import Results, Location, Occupy
from wtforms.validators import DataRequired
# a function that can be attached to a field to perform validation on the data submitted by the user.

class AnalysisForm(Form):
    room = SelectField("Room", validators=[DataRequired()])
    day = SelectField("Day", validators=[DataRequired()])
    time = SelectField("Time", validators=[DataRequired()])
    model_type = SelectField("Model", validators=[DataRequired()])
    
    # def __init__(self, rooms, days, times, model_types):
    def __init__(self, *args, **kwargs):
        super(AnalysisForm, self).__init__(*args, **kwargs)
        self.room.choices = [(i.room, i.room) for i in db.session.query(Location.room).distinct().order_by(Location.room)]
        self.day.choices = [("Monday", "Monday"), ("Tuesday", "Tuesday"), ("Wednesday", "Wednesday"), ("Thursday", "Thursday"), ("Friday", "Friday")]
        # self.day.choices = set([(get_day(i.date), get_day(i.date)) for i in db.session.query(Occupy.date).filter(or_(Occupy.occupancy.isnot(None), Occupy.authenticated_client_count.isnot(None))).distinct().order_by(Occupy.date)])
        self.time.choices = [(i.time, i.time) for i in db.session.query(Occupy.time).distinct().order_by(Occupy.time) if int(i.time[0:2]) >= 9 and int(i.time[0:2]) <= 16 and i.time[3:5] == "00"]
        self.model_type.choices = [(i.model_type, i.model_type) for i in db.session.query(Results.model_type).distinct().order_by(Results.model_type)]

