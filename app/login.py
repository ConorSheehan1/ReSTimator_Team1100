# source: http://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iii-web-forms 

from flask_wtf import Form
from wtforms import StringField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Email # validator, a function that can be attached to a field to perform validation on the data submitted by the user.

class LoginForm(Form):
	username = StringField('Username', validators=[DataRequired(), Email()]) # Required validator checks that the field is not submitted empty. There are many more validators included with Flask-WTF
	password = PasswordField('Password', validators=[DataRequired()])
	remember_me = BooleanField('remember_me', default=False)

'''source: http://flask.pocoo.org/snippets/64/
def __init__(self, *args, **kwargs):
Form.__init__(self, *args, **kwargs)
self.user = None

def validate(self):
rv = Form.validate(self)
if not rv:
return False

user = User.query.filter_by(username=self.username.data).first()
if user is None:
self.username.errors.append('Unknown username')
return False

if not user.check_password(self.password.data):
self.password.errors.append('Invalid password')
return False

self.user = user
return True'''