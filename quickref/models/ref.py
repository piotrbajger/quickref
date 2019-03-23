from ..extensions import db


class Ref(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bib_id = db.Column(db.String(32))
    entry_type = db.Column(db.Integer)
    title = db.Column(db.String(256), index=True)
    author = db.Column(db.String(256))
    year = db.Column(db.Integer)
    month = db.Column(db.Integer)
    # Article-specific
    journal = db.Column(db.String(128))
    pages = db.Column(db.String(16))
    volume = db.Column(db.String(8))
    number = db.Column(db.String(8))
    # Book-specific
    editor = db.Column(db.String(32))
    publisher = db.Column(db.String(64))
    edition = db.Column(db.String(16))
    series = db.Column(db.String(32))
    address = db.Column(db.String(96))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def to_dict(self):
        fields = Ref.get_fields_for_entry(self.entry_type, optional=True)

        return_dict = {
            "ENTRYTYPE": self.entry_type,
            "ID": self.bib_id,
        }

        for field in fields:
            if type(field) == str:
                val = self.__getattribute__(field)
                if val is not None:
                    return_dict[field] = str(val)
            else:
                for subf in field:
                    val = self.__getattribute__(subf)
                    if val is not None:
                        return_dict[subf] = str(val)

        return return_dict

    def __repr__(self):
        return f"<Ref: {self.title}>"

    ALLOWED_ENTRIES = ['article', 'book']

    ALLOWED_FIELDS = {
        'article': {
            'required': ['author', 'title', 'journal', 'year'],
            'optional': ['volume', 'number', 'pages', 'month']
        },
        'book': {
            'required': [['author', 'editor'], 'title', 'publisher', 'year'],
            'optional': [['volume', 'number'], 'series', 'address', 'edition',
                         'month']
        }
    }

    @staticmethod
    def get_fields_for_entry(entry_type, optional=False):
        """Returns a list of fields allowed for a given entry."""
        if entry_type not in Ref.ALLOWED_ENTRIES:
            raise ValueError(f"Entry type {entry_type} is not supported.")

        if optional:
            return (Ref.ALLOWED_FIELDS[entry_type]['required'] +
                    Ref.ALLOWED_FIELDS[entry_type]['optional'])
        else:
            return Ref.ALLOWED_FIELDS[entry_type]['required']


def ref_model_factory_from_form(form):
    """
        Returns a ref model based on entry_type and a RefEditForm.
    """
    fields = Ref.get_fields_for_entry(entry_type, optional=True)

    ref = Ref()
    ref.entry_type = entry_type

    for field in fields:
        if type(field) == str:
            ref.__setattr__(field, form.__getattribute__(field).data)
        elif type(field) == list:
            for or_field in field:
                ref.__setattr__(or_field,
                                form.__getattribute__(or_field).data)

    return ref


def ref_model_factory_from_dict(entry_type, field_vals):
    """Returns a ref model based on entry_type and a dict of fields."""
    fields = Ref.get_fields_for_entry(entry_type, optional=True)

    ref = Ref()
    ref.entry_type = entry_type
    ref.bib_id = field_vals["ID"]

    for field in fields:
        if type(field) == str:
            ref.__setattr__(field, field_vals.get(field))
        elif type(field) == list:
            for or_field in field:
                ref.__setattr__(or_field, field_vals.get(or_field))

    return ref


def ref_model_updater(ref, form):
    """Updates a ref based on form data."""
    fields = Ref.get_fields_for_entry(ref.entry_type,
                                      optional=True)
    if 'pages' in fields:
        form.pages.data = f"{form.pages_lo.data}--{form.pages_hi.data}"
        print(form.pages.data)

    for f in fields:
        if type(f) == str:
            ref.__setattr__(f, form.__getattribute__(f).data)
        elif type(f) == list:
            for or_f in f:
                ref.__setattr__(or_f, form.__getattribute__(or_f).data)

    return ref