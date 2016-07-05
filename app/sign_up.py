# source: http://flask.pocoo.org/docs/0.11/patterns/wtforms/
from flask_wtf import Form
from wtforms import StringField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo # validator, a function that can be attached to a field to perform validation on the data submitted by the user.

class RegistrationForm(Form):
    username = StringField('Email Address', [DataRequired(), Email()])
    password = PasswordField('New Password', [DataRequired(), EqualTo('confirm', message='Passwords don\'t match')])
    confirm = PasswordField('Repeat Password')
    accept_terms = BooleanField('I accept the terms and conditions', [DataRequired()])
    