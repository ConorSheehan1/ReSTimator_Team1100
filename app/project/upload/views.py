from flask import render_template, flash, redirect, request, Blueprint
from .forms import UploadForm
from flask.ext.login import login_required
from werkzeug import secure_filename
import os

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