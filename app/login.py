# source: http://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iii-web-forms 

from flask_wtf import Form
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired # validator, a function that can be attached to a field to perform validation on the data submitted by the user.

class LoginForm(Form):
    openid = StringField('openid', validators=[DataRequired()]) # Required validator checks that the field is not submitted empty. There are many more validators included with Flask-WTF
    remember_me = BooleanField('remember_me', default=False)