from quickref import app, db
from quickref.models.user import User


@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User
    }