from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField


class UploadBibFileForm(FlaskForm):
    filename = FileField()
    upload = SubmitField('Upload')