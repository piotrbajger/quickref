from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from ..extensions import db
from ..extensions import login_manager


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    refs = db.relationship('Ref', backref='owner', lazy='dynamic')

    def set_password(self, new_password):
        """Hashes and setts password."""
        self.password_hash = generate_password_hash(new_password)

    def check_password(self, password):
        """Checks if password matches the hashed password."""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User: {self.username}: {self.email}>"


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
