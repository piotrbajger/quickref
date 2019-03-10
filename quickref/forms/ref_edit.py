from bibtexmagic.bibtexmagic import BibTexMagic
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField
from wtforms import validators


class RefEditForm(FlaskForm):
    _CHOICES = list(zip(BibTexMagic.ALLOWED_ENTRIES, BibTexMagic.ALLOWED_ENTRIES))
    entry_type = SelectField('Type',
                             choices=_CHOICES,
                             validators=[validators.DataRequired()])
    title = StringField('Title', validators=[validators.DataRequired()])
    author = StringField('Author')
    journal = StringField('Journal')
    year = IntegerField('Year')
    month = IntegerField('Month', validators=[validators.optional()])
    pages_lo = IntegerField('Pages', validators=[validators.optional()])
    pages_hi = IntegerField('Pages', validators=[validators.optional()])
    pages = StringField('Pages')
    volume = StringField('Volume')
    number = StringField('Number')
    editor = StringField('Editor')
    publisher = StringField('Publisher')
    edition = StringField('Edition')
    series = StringField('Series')
    address = StringField('Address')

    submit = SubmitField("Update")

    def validate(self):
        """Custom form validator conditional on entry_type"""
        rv = FlaskForm.validate(self)
        if not rv:
            return False

        reqs = BibTexMagic.get_fields_for_entry(self.entry_type.data)
        valid = True

        for req_field in reqs:
            if type(req_field) == str:
                formfield = self.__getattribute__(req_field)
                data = formfield.data
                if not data:
                    formfield.errors.append("This field is required.")
                    valid = False
            elif type(req_field) == list:
                formfields = [self.__getattribute__(sub) for sub in req_field]
                if not any(formfield.data for formfield in formfields):
                    msg = "At least one of: " + \
                        ', '.join([r.capitalize() for r in req_field]) + \
                        "is required."

                    for formfield in formfields:
                        formfield.errors.append(msg)
                        valid = False

        if (not self.pages_lo.data and self.pages_hi.data) or \
           (not self.pages_hi.data and self.pages_lo.data):
            self.pages.errors.append("Both (or none) Pages fields required.")

        return valid

