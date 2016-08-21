# source: http://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iii-web-forms 
from flask_wtf import Form, RecaptchaField
from wtforms import StringField, PasswordField, BooleanField, validators
from project import db, app
from project.models import Users
# validator, a function that can be attached to a field to perform validation on the data submitted by the user.


def ucd_email(form, field):
    # if not field.data.endswith('@ucd.ie'):
    if not field.data.endswith(app.config["ACCEPTABLE_SUFFIX"]):
        raise validators.ValidationError('Please use a ucd staff email (example@ucd.ie)')


def already_signed_up(form, field):
    # if the email is already in the database raise an exception
    # is not doesn't work for some reason so use !=[]
    if db.session.query(Users).filter(Users.username == field.data).all() !=[]:
        if Users.query.filter(Users.username == field.data).first().confirmed:
            raise validators.ValidationError('This email is already signed up and confirmed.')
        else:
            # if the user is not confirmed tell them to reset  their password to activate account
            raise validators.ValidationError('This email is already signed up.'
                                  ' If your confirmation link has expired,'
                                  ' please reset your password to activate your account.')


def not_signed_up(form, field):
    if db.session.query(Users).filter(Users.username == field.data).all() == []:
        raise validators.ValidationError('This email is not signed up yet.')


def verified(form, field):
    # if email is not in db
    if not db.session.query(Users).filter(Users.username == field.data).first():
        raise validators.ValidationError("Please register your email using the sign up page")
    # if email is not confirmed
    elif not db.session.query(Users).filter(Users.username == field.data).first().confirmed:
        raise validators.ValidationError("Please verify your email")

def valid_password_content(form, field):
    if not any(char.isdigit() for char in field.data):
        raise validators.ValidationError("Please include at least one number in your password")
    if not any(char.isalpha() for char in field.data):
        raise validators.ValidationError("Please include at least one letter in your password")


class LoginForm(Form):
    username = StringField('Username', [validators.DataRequired(), validators.Email(), ucd_email, verified])
    # Required validator checks that the field is not submitted empty.
    # There are many more validators included with Flask-WTF
    password = PasswordField('Password', [validators.DataRequired()])


class SignUpForm(Form):
    username = StringField('Email Address', [validators.DataRequired(), validators.Email(), ucd_email, already_signed_up])
    password = PasswordField('Password', [validators.DataRequired(), validators.EqualTo('confirm', message='Passwords need to match'),
                                          validators.Length(min=8), valid_password_content])
    confirm = PasswordField('Repeat Password')
    accept_terms = BooleanField('I accept the terms and conditions', [validators.DataRequired()])
    recaptcha = RecaptchaField()


class ResetForm(Form):
    # need to be verified to reset?
    username = StringField('Email Address', [validators.DataRequired(), validators.Email(), ucd_email, not_signed_up])
    password = PasswordField('New Password', [validators.DataRequired(), validators.EqualTo('confirm', message='Passwords need to match'),
                                              validators.Length(min=8), valid_password_content])
    confirm = PasswordField('Repeat Password')
    recaptcha = RecaptchaField()

