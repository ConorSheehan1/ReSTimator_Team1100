from flask import render_template, flash, redirect, request, Blueprint
from .forms import UploadForm, GTForm, ModuleForm, LocationForm, AddUserForm
from flask.ext.login import login_required
from werkzeug import secure_filename
import os
from project import db, app, admin_permission, normal_permission
from project.models import *
from sqlalchemy import exists
from legacy_into_db import legacy
from analysis import analysis

upload_blueprint = Blueprint("upload", __name__, template_folder="templates")

@upload_blueprint.route("/admin", methods=["GET", "POST"])
@login_required
@admin_permission.require(http_exception=403)
def admin_options():
    '''Administrator options view'''
    
    pg_name = "Admin Options"
    return render_template("admin_options.html", pg_name=pg_name)

@upload_blueprint.route("/upload", methods=["GET", "POST"])
@login_required
@admin_permission.require(http_exception=403)
def upload():
    """Upload view"""
    
    pg_name = "Upload"
    form = UploadForm()
#     filename = ""
#     print("test1")
#     if request.method == "POST" and form.validate_on_submit():
#         print('test2')
#         print(form.upload)
#         print(request.files['file'].filename)
#         filename = secure_filename(form.upload.data.filename)
#         print(filename, app.config['UPLOAD_FOLDER'])
#         form.upload.data.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#         image_data = request.FILES[form.image.name].read()
#         open(os.path.join(UPLOAD_PATH, form.image.data), 'w').write(image_data)
#     return render_template('upload.html', pg_name=pg_name, form=form, filename=filename)
    # For a given file, return whether it's an allowed type or not
    def allowed_file(filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

    filename = ''
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No file selected. Please select a file to upload.')
            return redirect(request.url)
        if file:
            if allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                # Add to database
                legacy()
                # Do analysis for results table
                analysis("../../project/sample.db")
                flash('Uploaded ' + filename)
            else:
                flash('File must be .csv or .zip')
    return render_template("upload.html", pg_name=pg_name, form=form)

@upload_blueprint.route("/add_occupancy", methods=["GET", "POST"])
@login_required
def upload_GT():
    '''Upload Ground Truth view'''
    
    pg_name = "Input Occupancy Data"
    form = GTForm()
    
    if request.method == "POST" and form.validate_on_submit():
        # get date in same format as date in database
        date = form.date.data
        date = date[6:] + date[2:6] + date[0:2]
        occupancy = float(form.occupancy.data)
        # Check if row already exists in database
        q = Occupy.query.filter_by(room = form.room.data, date = date, time = form.time.data)
        (already_exists, ), = db.session.query(q.exists()).all() # unpacking the list and tuple into the variable
        if not already_exists:
            # prepare SQLAlchemy statement
            row = Occupy(room = form.room.data, date = date, time = form.time.data, occupancy = occupancy,
                         module_code = form.module_code.data, associated_client_count = None, authenticated_client_count = None)
            db.session.add(row)
            db.session.commit() # committing data to database
            print('row added')
            flash('Thank you! Your data has been recorded.')
        else:
            print('row already exists')
            flash('Your data has already been recorded. Please check that you selected the correct information for Room, Date and Time.')
    return render_template("add_occupancy.html", pg_name=pg_name, form=form)

@upload_blueprint.route("/add_module", methods=["GET", "POST"])
@login_required
@admin_permission.require(http_exception=403)
def add_module():
    '''Administrator add module information view'''
    
    pg_name = "Add Module Info"
    form = ModuleForm()
    
    if request.method == "POST" and form.validate_on_submit():
        # Check if row already exists in database
        q = Module.query.filter_by(module_code = form.module.data)
        (already_exists, ), = db.session.query(q.exists()).all() # unpacking the list and tuple into the variable
        if not already_exists:
            # prepare SQLAlchemy statement
            row = Module(module_code = form.module.data, reg_students = form.students.data)
            db.session.add(row)
            db.session.commit() # committing data to database
            print('row added')
            flash('Thank you! Your data has been recorded.')
        else:
            print('row already exists')
            flash('Your data has already been recorded. Please check that you selected the correct information for Module Code.')
    return render_template("add_module.html", pg_name=pg_name, form=form)

@upload_blueprint.route("/add_location", methods=["GET", "POST"])
@login_required
@admin_permission.require(http_exception=403)
def add_location():
    '''Administrator add location information view'''
    
    pg_name = "Add Location Info"
    form = LocationForm()
    
    if request.method == "POST" and form.validate_on_submit():
        # Check if row already exists in database
        q = Location.query.filter_by(campus = form.campus.data, building = form.building.data, room = form.room.data)
        (already_exists, ), = db.session.query(q.exists()).all() # unpacking the list and tuple into the variable
        if not already_exists:
            # prepare SQLAlchemy statement
            row = Location(campus = form.campus.data, building = form.building.data, room = form.room.data, capacity = form.capacity.data)
            db.session.add(row)
            db.session.commit() # committing data to database
            print('row added')
            flash('Thank you! Your data has been recorded.')
        else:
            print('row already exists')
            flash('Your data has already been recorded. Please check that you selected the correct information for \
            Campus, Building, and Room.')
    return render_template("add_location.html", pg_name=pg_name, form=form)

@upload_blueprint.route("/add_user", methods=["GET", "POST"])
@login_required
@admin_permission.require(http_exception=403)
def add_user():
    '''Add user view'''
    pg_name = "Add User"
    form = AddUserForm() # create instance of RegistrationForm
    # flash("Please Register")
    if request.method == "POST" and form.validate_on_submit():
        user = Users(username=form.username.data, password=form.password.data, role=form.role.data) 
        # user = Users(username=form.username.data, password=form.password.data, confirmed=False) 
        db.session.add(user)
        db.session.commit()
        flash("Successfully Registered New User")
    return render_template("add_user.html", pg_name=pg_name, form=form)