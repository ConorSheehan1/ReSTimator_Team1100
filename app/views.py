from flask import render_template, flash, redirect
from app import restimatorApp
from .login import LoginForm

@restimatorApp.route("/")
@restimatorApp.route("/index")
def template():
    '''Render html template'''
    user = {'username': 'Team 1100'}  # fake user
    return render_template("home.html", username = user) # function takes a template filename and a variable list of template args and returns the rendered template (invokes Jinja2 templating engine)

@restimatorApp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for OpenID="%s", remember_me=%s' %
              (form.openid.data, str(form.remember_me.data)))
        return redirect('/index')
    return render_template('login.html', title='Sign In', form=form)