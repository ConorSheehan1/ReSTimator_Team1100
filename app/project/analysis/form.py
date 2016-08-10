from project import db
from sqlalchemy import *
from flask_wtf import Form
from wtforms import SelectField, SubmitField, StringField
# from wtforms.fields.html5 import DateField
from project.models import Results, Location, Occupy
from wtforms.validators import DataRequired

class AnalysisForm(Form):
    model_type = SelectField("Model", validators=[DataRequired()])  
    campus = SelectField("Campus", validators=[DataRequired()])
    building = SelectField("Building", validators=[DataRequired()])
    room = SelectField("Room", validators=[DataRequired()])
    time = SelectField("Time", validators=[DataRequired()])
    date = StringField('Pick a Date', validators=[DataRequired()])


    def __init__(self, *args, **kwargs):
        super(AnalysisForm, self).__init__(*args, **kwargs)
        self.model_type.choices = [(i.model_type, i.model_type) for i in db.session.query(Results.model_type).distinct().order_by(Results.model_type)]
        self.campus.choices = [(i.campus, i.campus) for i in db.session.query(Location.campus).distinct().order_by(Location.campus)]
        self.building.choices = [(i.building, i.building) for i in db.session.query(Location.building).distinct().order_by(Location.building)]
        self.room.choices = [(i.room, i.room) for i in db.session.query(Location.room).distinct().order_by(Location.room)]
        self.time.choices = [(i.time, i.time) for i in db.session.query(Occupy.time).distinct().order_by(Occupy.time) if int(i.time[0:2]) >= 9 and int(i.time[0:2]) <= 16 and i.time[3:5] == "00"]
