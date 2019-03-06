import flask
from flask_login import current_user, login_user, logout_user, login_required

from ..extensions import db
from ..models import user
from ..models.user import User
from ..models.ref import Ref
from ..forms.upload_bib import UploadBibFileForm
from ..forms.ref_edit import RefEditForm


refs = flask.Blueprint('refs', __name__)


@refs.route('/refs', methods=['GET'])
@login_required
def index():
    refs = Ref.query.filter_by(user_id=current_user.id)
    
    upload_form = UploadBibFileForm()

    return flask.render_template('refs.html', title="Refs", refs=refs,
                                 upload_form=upload_form)


@refs.route('/ref/<ref_id>', methods=['GET'])
@login_required
def ref(ref_id):
    ref = Ref.query.filter_by(
        user_id=current_user.id,
        id=ref_id
    ).first_or_404()
    
    pages = ref.pages.replace("--", "-")
    page_lo, page_hi = pages.split("-")

    edit_form = RefEditForm(
        title=ref.title,
        authors=ref.authors,
        journal=ref.journal,
        year=ref.year,
        pages_lo=page_lo,
        pages_hi=page_hi
    )

    return flask.render_template('ref.html', title="Edit Ref",
                                 ref=ref, edit_form=edit_form)

@refs.route('/ref/<ref_id>', methods=['POST'])
@login_required
def ref_post(ref_id):
    form = RefEditForm()

    if form.validate_on_submit():
        ref = Ref.query.filter_by(
            user_id=current_user.id,
            id=ref_id
        ).first_or_404()

        print(form.title)
        ref.title = form.title.data
        ref.authors = form.authors.data
        ref.journal = form.journal.data
        ref.year = form.year.data
        ref.pages = f"{form.pages_lo.data}--{form.pages_hi.data}"

        db.session.commit()
        ref_url = flask.url_for('refs.index')
        flask.flash(flask.Markup(
            f"Reference updated. <a href=\"{ref_url}\">Go back to Refs</a>"
        ))

    return flask.redirect(flask.url_for('refs.ref', ref_id=ref_id))