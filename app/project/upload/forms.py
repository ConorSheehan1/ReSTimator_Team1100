from project import db
from project.models import Location, Module
from flask_wtf import Form
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import SelectField, StringField, IntegerField, PasswordField, validators
from project.users.forms import ucd_email, already_signed_up


class UploadForm(Form):
    """Form for allowing user to upload files."""
    
    upload = FileField('file', validators=[
        FileRequired('You have not selected a file to upload. Please select a file.'),
        FileAllowed(['zip', 'csv', 'xlsx'], 'File type not allowed')
    ])


class GTForm(Form):
    """Form allowing user to add single record of Ground Truth data to database"""
    
    room = SelectField("Room", [validators.DataRequired()])
    date = StringField('Pick a Date', [validators.DataRequired()])
    time = SelectField("Time", [validators.DataRequired()], choices = [("09:00", "09:00"), ("10:00", "10:00"), ("11:00", "11:00"),
                                          ("12:00", "12:00"), ("13:00", "13:00"), ("14:00", "14:00"),
                                          ("15:00", "15:00"), ("16:00", "16:00")])
    module_code = SelectField("Module Code", [validators.DataRequired()])
    occupancy = SelectField("Occupancy", [validators.DataRequired()], choices = [("0", "0%"), ("0.125", "12.5%"), ("0.25", "25%"), ("0.375", "37.5%"), ("0.5", "50%"), 
                                                                                 ("0.625", "62.5%"), ("0.75", "75%"), ("0.875", "87.5%"), ("1", "100%")])
    
    def __init__(self, *args, **kwargs):
        super(GTForm, self).__init__(*args, **kwargs)
        self.room.choices = [(i.room, i.room) for i in db.session.query(Location.room).distinct().order_by(Location.room)]
        self.module_code.choices = [(i.module_code, i.module_code) for i in db.session.query(Module.module_code).distinct().order_by(Module.module_code)]


class ModuleForm(Form):
    """Form allowing user to add Module details to database"""
    
    module = StringField('Module Code', [validators.Length(min=7, max=12)])
    students = IntegerField('Registered Students', [validators.DataRequired()])


class LocationForm(Form):
    """Form allowing user to add Location details to database"""
    
    campus = StringField('Campus', [validators.DataRequired()])
    building = StringField('Building', [validators.DataRequired()])
    room = StringField('Room', [validators.DataRequired()])
    capacity = IntegerField('Capacity', [validators.DataRequired()])


class AddUserForm(Form):
    """Form allowing user to add new user to database"""
    
    username = StringField('Email Address', [validators.DataRequired(), validators.Email(), ucd_email, already_signed_up])
    role = SelectField("Role", [validators.DataRequired()], choices = [("normal", "Normal"), ("admin", "Admin")])
    password = PasswordField('New Password', [validators.DataRequired(), validators.EqualTo('confirm', message='Passwords need to match')])
    confirm = PasswordField('Repeat Password')