from flask_wtf import Form
from flask_wtf.file import FileField, FileAllowed, FileRequired

class UploadForm(Form):
    upload = FileField('file', validators=[
#         FileRequired('Please select a file to upload'),
        FileAllowed(['txt', 'csv', 'xlsx'], 'File type not allowed')
    ])