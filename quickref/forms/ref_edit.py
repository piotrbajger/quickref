from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField
from wtforms import validators

from ..models.ref import Ref


class RefEditForm(FlaskForm):
    entry_type = StringField('Type', validators=[validators.DataRequired()])
    bib_key = StringField('Key')
    title = StringField('Title', validators=[validators.optional()])
    author = StringField('Author', validators=[validators.optional()])
    journal = StringField('Journal', validators=[validators.optional()])
    year = IntegerField('Year', validators=[validators.optional()])
    month = IntegerField('Month', validators=[validators.optional()])
    pages_lo = IntegerField('Pages', validators=[validators.optional()])
    pages_hi = IntegerField('Pages', validators=[validators.optional()])
    pages = StringField('Pages', validators=[validators.optional()])
    volume = StringField('Volume', validators=[validators.optional()])
    number = StringField('Number', validators=[validators.optional()])
    editor = StringField('Editor', validators=[validators.optional()])
    publisher = StringField('Publisher', validators=[validators.optional()])
    edition = StringField('Edition', validators=[validators.optional()])
    series = StringField('Series', validators=[validators.optional()])
    address = StringField('Address', validators=[validators.optional()])

    submit = SubmitField("Update")

    def validate(self):
        """Custom form validator conditional on entry_type"""
        rv = FlaskForm.validate(self)
        print(self.entry_type.data)
        if not rv:
            return False

        reqs = Ref.get_fields_for_entry(self.entry_type.data)
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
        return valid

        if (not self.pages_lo.data and self.pages_hi.data) or \
           (not self.pages_hi.data and self.pages_lo.data):
            self.pages.errors.append("Both (or none) Pages fields required.")


