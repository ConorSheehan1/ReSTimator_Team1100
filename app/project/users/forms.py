# source: http://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iii-web-forms 
from flask_wtf import Form, RecaptchaField
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from project import db
from project.models import Users
# validator, a function that can be attached to a field to perform validation on the data submitted by the user.


def ucd_email(form, field):
    # only accept emails ending in @ucd.ie
    if not field.data.endswith('@ucd.ie'):
        raise ValidationError('Please use a ucd staff email (example@ucd.ie)')


def already_signed_up(form, field):
    # if the email is already in the database raise an exception
    # is not doesn't work for some reason so use !=[]
    if db.session.query(Users).filter(Users.username == field.data).all() !=[]:
        raise ValidationError('This email is already signed up')


class LoginForm(Form):
    username = StringField('Username', validators=[DataRequired(), Email(), ucd_email])
    # Required validator checks that the field is not submitted empty.
    # There are many more validators included with Flask-WTF
    password = PasswordField('Password', validators=[DataRequired()])


class SignUpForm(Form):
    username = StringField('Email Address', [DataRequired(), Email(), ucd_email, already_signed_up])
    password = PasswordField('New Password', [DataRequired(), EqualTo('confirm', message='Passwords need to match')])
    confirm = PasswordField('Repeat Password')
    accept_terms = BooleanField('I accept the terms and conditions', [DataRequired()])
    recaptcha = RecaptchaField()
