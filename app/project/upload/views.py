from flask import render_template, flash, redirect, request, Blueprint
from .forms import UploadForm, GTForm
from flask.ext.login import login_required
from werkzeug import secure_filename
import os
from project import db
from project.models import *
from sqlalchemy import exists

upload_blueprint = Blueprint("upload", __name__, template_folder="templates")


@upload_blueprint.route("/upload", methods=["GET", "POST"])
@login_required
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
#         print(filename, restimatorApp.config['UPLOAD_FOLDER'])
#         form.upload.data.save(os.path.join(restimatorApp.config['UPLOAD_FOLDER'], filename))
#         image_data = request.FILES[form.image.name].read()
#         open(os.path.join(UPLOAD_PATH, form.image.data), 'w').write(image_data)
#     return render_template('upload.html', pg_name=pg_name, form=form, filename=filename)
    # For a given file, return whether it's an allowed type or not
    def allowed_file(filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1] in restimatorApp.config['ALLOWED_EXTENSIONS']

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
                file.save(os.path.join(restimatorApp.config['UPLOAD_FOLDER'], filename))
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
        date = str(form.date.data.strftime('%x'))
        date = int('20' + date[6:] + date[0:2] + date[3:5])
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
    return render_template("add_occupancy.html", pg_name=pg_name, form=form, query=query)