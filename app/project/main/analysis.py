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
    hourly_time = SelectField("Time", validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super(AnalysisForm, self).__init__(*args, **kwargs)
        # self.day.choices = [(i.day ,i.day) for i in db.session.query(Results.day).distinct().order_by(Results.day)]
        # self.time.choices = [(i.time ,i.time) for i in db.session.query(Results.time).distinct().order_by(Results.time)]
        # self.module.choices = [(i.module ,i.module) for i in db.session.query(Results.module).distinct().order_by(Results.module)]
        self.room.choices = [(i.room, i.room) for i in db.session.query(Results.room).distinct().order_by(Results.room)]
        self.day.choices = [(i.day, i.day) for i in db.session.query(Results.day).distinct().order_by(Results.day)]
        self.hourly_time.choices = [(i.hourly_time, i.hourly_time) for i in db.session.query(Results.hourly_time).distinct().order_by(Results.hourly_time)]
