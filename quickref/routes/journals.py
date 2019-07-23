import json

import editdistance
import flask
from flask_login import login_required
from sqlalchemy import func

from ..models.journal import Journal


journals = flask.Blueprint('journals', __name__)


@journals.route('/lookup', methods=['GET'])
@login_required
def lookup():
    MAX_RESULTS = 10
    typed = flask.request.args['journal_typed'].lower()

    result = Journal.query.filter(
        func.lower(Journal.name).like(f"%{typed}%")
    ).all()

    names = [r.name for r in result]
    dists = [editdistance.eval(typed, name.lower()) for name in names]

    # Sort the names by Levenshtein distance
    response = list(zip(names, dists))
    response.sort(key=lambda x: x[1])
    response = [r[0] for r in response]
    response = response[:MAX_RESULTS]

    return json.dumps(response)