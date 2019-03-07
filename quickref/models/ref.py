from ..extensions import db


class Ref(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), index=True)
    authors = db.Column(db.String(256))
    journal = db.Column(db.String(128))
    year = db.Column(db.Integer)
    pages = db.Column(db.String(16))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f"<Ref: {self.title}>"
