from project import db
from project.models import Location, Module
from flask_wtf import Form
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import SelectField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import DateField

class UploadForm(Form):
    upload = FileField('file', validators=[
#         FileRequired('Please select a file to upload'),
        FileAllowed(['txt', 'csv', 'xlsx'], 'File type not allowed')
    ])
    
class GTForm(Form):
    room = SelectField("Room", validators=[DataRequired()])
    date = DateField('Pick a Date', format="%m/%d/%Y")
    time = SelectField("Time", choices = [("09:00", "09:00"), ("10:00", "10:00"), ("11:00", "11:00"),
                                          ("12:00", "12:00"), ("13:00", "13:00"), ("14:00", "14:00"),
                                          ("15:00", "15:00"), ("16:00", "16:00")], validators=[DataRequired()])
    module_code = SelectField("Module Code", validators=[DataRequired()])
    occupancy = SelectField("Occupancy", choices = [("0", "0%"), ("0.25", "25%"), ("0.5", "50%"), ("0.75", "75%"), ("1", "100%")],
                            validators=[DataRequired()])
    
    def __init__(self, *args, **kwargs):
        super(GTForm, self).__init__(*args, **kwargs)
        self.room.choices = [(i.room, i.room) for i in db.session.query(Location.room).distinct().order_by(Location.room)]
        self.module_code.choices = [(i.module_code, i.module_code) for i in db.session.query(Module.module_code).distinct().order_by(Module.module_code)]     