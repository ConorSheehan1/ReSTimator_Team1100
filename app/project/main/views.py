from flask import render_template, flash, redirect, url_for, request, Blueprint
from flask.ext.login import login_required
from project import db
from project.models import *
from werkzeug import secure_filename
from .upload import UploadForm
from project import restimatorApp
import os


main_blueprint = Blueprint("main", __name__, template_folder="templates")

# VIEWS: handlers that respond to requests from browsers.
# Flask handlers are written as functions (each view function is mapped to one or more request URLs)


@main_blueprint.route("/")
@main_blueprint.route("/home", methods=["GET", "POST"])
@login_required
def home():
    '''home view'''
    pg_name = "Home" 
    random = db.session.query(Users).all()
    return render_template("home.html", pg_name=pg_name, random=random)
    # function takes a template filename and a variable list of template args and returns the rendered template
    #  (invokes Jinja2 templating engine)

@main_blueprint.route("/about")
def about():
    '''about view'''
    pg_name = "About" 
    return render_template("about.html", pg_name=pg_name)


@main_blueprint.route("/data")
@login_required
def data():
    '''data view'''
    pg_name = "Data" 
    return render_template("data.html", pg_name=pg_name)


@main_blueprint.route("/contact")
def contact():
    '''contact view'''
    pg_name = "Contact" 
    return render_template("contact.html", pg_name=pg_name)

# @csrf.error_handler
# def csrf_error(reason):
#     return render_template('csrf_error.html', reason=reason), 400

@main_blueprint.route("/upload", methods=["GET", "POST"])
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
                flash('File must be .csv or .xlsx')
    return render_template("upload.html", pg_name=pg_name, form=form)