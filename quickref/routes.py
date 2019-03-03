import flask

from . import app


@app.route('/index')
@app.route('/')
def index():
    return flask.render_template('index.html', title="Home")