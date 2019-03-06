from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired


class RefEditForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    authors = StringField('Authors', validators=[DataRequired()])
    journal = StringField('Journal')
    year = IntegerField('Year')
    pages_lo = IntegerField('Pages')
    pages_hi = IntegerField('Pages')

    submit = SubmitField("Update")
