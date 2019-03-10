from bibtexmagic.bibtexmagic import BibTexMagic
from ..extensions import db


class Ref(db.Model):
    id = db.Column(db.Integer, primary_key=True)
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

    def __repr__(self):
        return f"<Ref: {self.title}>"


def ref_model_factory_from_form(form):
    """
        Returns a ref model based on entry_type and a RefEditForm.
    """
    fields = BibTexMagic.get_fields_for_entry(entry_type, optional=True)

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
    fields = BibTexMagic.get_fields_for_entry(entry_type, optional=True)

    ref = Ref()
    ref.entry_type = entry_type

    for field in fields:
        if type(field) == str:
            ref.__setattr__(field, field_vals.get(field))
        elif type(field) == list:
            for or_field in field:
                ref.__setattr__(or_field, field_vals.get(or_field))

    return ref


def ref_model_updater(ref, form):
    """Updates a ref based on form data."""
    fields = BibTexMagic.get_fields_for_entry(ref.entry_type,
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