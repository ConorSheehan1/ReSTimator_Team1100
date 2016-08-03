from project import db
from flask_wtf import Form
from wtforms import SelectField
from project.models import Results
from wtforms.validators import DataRequired
# from wtforms.validators import DataRequired, Email, EqualTo # validator,
# a function that can be attached to a field to perform validation on the data submitted by the user.


class AnalysisForm(Form):
    room = SelectField("Room", validators=[DataRequired()])
    day = SelectField("Day", validators=[DataRequired()])
    time = SelectField("Time", validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super(AnalysisForm, self).__init__(*args, **kwargs)
        self.room.choices = [(i.room, i.room) for i in db.session.query(Results.room).distinct().order_by(Results.room)]
        self.time.choices = [(i.time, i.time) for i in db.session.query(Results.time).distinct().order_by(Results.time)]
        days_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        days = [i.day for i in db.session.query(Results.day).distinct()]
        self.day.choices = [(day, day) for day in sorted(days, key=lambda o: days_order.index(o))]
