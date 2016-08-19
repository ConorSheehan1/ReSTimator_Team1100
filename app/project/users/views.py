from flask import render_template, flash, redirect, url_for, request, Blueprint, session
from .forms import LoginForm, SignUpForm, ResetForm
from .token import generate_confirmation_token, confirm_token
from .email import send_email
from flask.ext.login import login_user, login_required, logout_user
from project.models import Users
from project import db, app
import datetime
from flask.ext.principal import Identity, RoleNeed, UserNeed, Permission, identity_changed, identity_loaded

users_blueprint = Blueprint("users", __name__, template_folder="templates")


@users_blueprint.route("/login", methods=["GET", "POST"]) # route for handling the login page logic. view function accepts both GET and POST requests
def login():
    '''form view'''
    pg_name = "Login"
    error = None
    form = LoginForm(request.form) # create instance of LoginForm request.form
    if request.method == "POST" and form.validate_on_submit():
        user = Users.query.filter_by(username=request.form["username"]).first()
        if user is not None and user.check_password(form.password.data): 
            login_user(user) # function manages session cookie. User model needs to be updated to allow user to be considered active
            # Tell Flask-Principal the identity changed
            identity_changed.send(app, identity=Identity(user.username))
            flash("User %s logged in successfully" % (form.username.data)) # returns a message on next page to user
            return redirect(url_for("main.home")) # redirect tells the client web browser to navigate to a different page
        else:
            error = "Invalid user credentials. Please try again."
    return render_template("login.html", pg_name=pg_name, title="Sign In", form=form, error=error) # pass LoginForm object to template


@users_blueprint.route("/logout")
@login_required
def logout():
    ''''''
    logout_user() # logs out user and cleans out session cookie
    # Remove session keys set by Flask-Principal
    for key in ('identity.name', 'identity.auth_type'):
        session.pop(key, None)
    flash("User logged out")
    return redirect(url_for("users.login"))


@users_blueprint.route("/sign_up", methods=["GET", "POST"])
def sign_up():
    '''Sign up view'''
    pg_name = "Sign Up" 
    form = SignUpForm() # create instance of RegistrationForm
    # flash("Please Register")
    if request.method == "POST" and form.validate_on_submit():
        # don't need to pass confirmed=False because it's the default
        user = Users(username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()

        token = generate_confirmation_token(user.username)
        confirm_url = url_for('users.confirm_email', token=token, _external=True)
        html = render_template('activate_email.html', confirm_url=confirm_url)
        subject = "Please confirm your email"
        send_email(user.username, subject, html)

        login_user(user)
        flash('A confirmation link has been sent to your email address. The link will expire in one hour.', 'success')
        # flash("Successfully Registered")
        return redirect(url_for("main.home"))
    return render_template("sign_up.html", pg_name=pg_name, form=form)


@users_blueprint.route('/reset', methods=["GET", "POST"])
def reset():
    pg_name = 'reset'
    form = ResetForm()
    if request.method == "POST" and form.validate_on_submit():
        token = generate_confirmation_token(form.username.data + ",+," + form.password.data)
        reset_url = url_for('users.reset_password', token=token, _external=True)
        html = render_template('reset_email.html', reset_url=reset_url)
        subject = "Reset password"
        send_email(form.username.data, subject, html)

        flash('A reset link has been sent to your email address. The link will expire in one hour.', 'success')
    return render_template("reset.html", pg_name=pg_name, form=form)


@users_blueprint.route('/confirm/<token>')
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        flash('The confirmation link is invalid or has expired.', 'danger')
    user = Users.query.filter_by(username=email).first_or_404()
    if user.confirmed:
        flash('Account already confirmed. Please login.', 'success')
    else:
        user.confirmed = True
        user.confirmed_on = datetime.datetime.now()
        db.session.add(user)
        db.session.commit()
        flash('You have confirmed your account. Thanks!', 'success')
    return redirect(url_for('main.home'))


@users_blueprint.route('/reset_password/<token>')
def reset_password(token):
    try:
        data_string = confirm_token(token)
        data_list = data_string.split(",+,")
        email = data_list[0]
        password = data_list[1]
    except:
        flash('The reset link is invalid or has expired.', 'danger')
    try:
        user = Users.query.filter_by(username=email).first_or_404()
        user.password = user.set_password(password)
        # click
        user.verified = True
        db.session.add(user)
        db.session.commit()
        flash('You have reset your password!', 'success')
        login_user(user)
    except:
        flash('Error resetting password', 'danger')
    return redirect(url_for('main.home'))
