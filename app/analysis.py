from flask_wtf import Form
from wtforms import SelectField
from .tables import Results
from wtforms.validators import DataRequired
# from wtforms.validators import DataRequired, Email, EqualTo # validator, a function that can be attached to a field to perform validation on the data submitted by the user.

class AnalysisForm(Form):
    day = SelectField("Day", validators=[DataRequired()])
    time = SelectField("Time", validators=[DataRequired()])
    module = SelectField("Module", validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
    	super(AnalysisForm, self).__init__(*args, **kwargs)
    	# self.day.choices = [i.day for i in Results.query.order_by(Results.day.distinct())]
    	self.day.choices = [(i.day ,i.day) for i in Results.query.order_by(Results.day)]
    	self.time.choices = [(i.time, i.time) for i in Results.query.order_by(Results.time)]
    	self.module.choices = [(i.module, i.module) for i in Results.query.order_by(Results.module)]

