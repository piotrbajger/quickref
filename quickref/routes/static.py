import flask
from flask_login import current_user, login_user, logout_user

from ..models.user import User
from ..forms.login import LoginForm


static = flask.Blueprint('static', __name__)


@static.route('/index')
@static.route('/')
def index():
    return flask.render_template('index.html', title="Home")


@static.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return flask.redirect(flask.url_for('static.index'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flask.flash("Invalid username or password.")
            return flask.redirect(flask.url_for('static.login'))

        login_user(user, remember=form.remember.data)
        flask.flash(f"Welcome {form.username.data}!")

        next_page = flask.request.args.get('next')
        if not next_page or flask.url_parse(next_page).netloc != '':
            next_page = flask.url_for('static.index')

        return flask.redirect(next_page)

    return flask.render_template('login.html', title="Login", form=form)


@static.route('/logout')
def logout():
    logout_user()
    return flask.redirect(flask.url_for('static.index'))
