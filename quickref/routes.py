import flask

from . import app
from .forms.login import LoginForm


@app.route('/index')
@app.route('/')
def index():
    return flask.render_template('index.html', title="Home")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        flask.flash(f"Welcome {form.username}!")
        return flask.redirect(flask.url_for('index'))

    return flask.render_template('login.html', title="Login", form=form)    