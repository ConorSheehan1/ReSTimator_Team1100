# source: http://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iii-web-forms 
from flask_wtf import Form, RecaptchaField
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from project import db, app
from project.models import Users
# validator, a function that can be attached to a field to perform validation on the data submitted by the user.


def ucd_email(form, field):
    # if not field.data.endswith('@ucd.ie'):
    if not field.data.endswith(app.config["ACCEPTABLE_SUFFIX"]):
        raise ValidationError('Please use a ucd staff email (example@ucd.ie)')


def already_signed_up(form, field):
    # if the email is already in the database raise an exception
    # is not doesn't work for some reason so use !=[]
    if db.session.query(Users).filter(Users.username == field.data).all() !=[]:
        if Users.query.filter(Users.username == field.data).first().confirmed:
            raise ValidationError('This email is already signed up and confirmed.')
        else:
            # if the user is not confirmed tell them to reset  their password to activate account
            raise ValidationError('This email is already signed up.'
                                  ' If your confirmation link has expired,'
                                  ' please reset you password to activate your account.')


def not_signed_up(form, field):
    if db.session.query(Users).filter(Users.username == field.data).all() == []:
        raise ValidationError('This email is not signed up yet.')


def verified(form, field):
    # if email is not in db
    if not db.session.query(Users).filter(Users.username == field.data).first():
        raise ValidationError("Please register your email using the sign up page")
    # if email is not confirmed
    elif not db.session.query(Users).filter(Users.username == field.data).first().confirmed:
        raise ValidationError("Please verify your email")


class LoginForm(Form):
    username = StringField('Username', validators=[DataRequired(), Email(), ucd_email, verified])
    # Required validator checks that the field is not submitted empty.
    # There are many more validators included with Flask-WTF
    password = PasswordField('Password', validators=[DataRequired()])


class SignUpForm(Form):
    username = StringField('Email Address', [DataRequired(), Email(), ucd_email, already_signed_up])
    password = PasswordField('Password', [DataRequired(), EqualTo('confirm', message='Passwords need to match')])
    confirm = PasswordField('Repeat Password')
    accept_terms = BooleanField('I accept the terms and conditions', [DataRequired()])
    recaptcha = RecaptchaField()


class ResetForm(Form):
    # need to be verified to reset?
    username = StringField('Email Address', [DataRequired(), Email(), ucd_email, not_signed_up])
    password = PasswordField('New Password', [DataRequired(), EqualTo('confirm', message='Passwords need to match')])
    confirm = PasswordField('Repeat Password')
    recaptcha = RecaptchaField()

