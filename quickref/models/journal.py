from ..extensions import db


class Journal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True, unique=True)
    abbrev = db.Column(db.String(128), index=True)

    def __repr__(self):
        return f"<Journal: {self.name} ({self.abbrev})>"

