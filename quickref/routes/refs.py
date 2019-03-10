import flask
from flask_login import current_user, login_required

from bibtexmagic.bibtexmagic import BibTexMagic

from ..extensions import db
from ..models.ref import Ref
from ..models.ref import ref_model_updater, ref_model_factory_from_dict
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

    if ref.pages:
        pages = ref.pages.replace("--", "-")
        page_lo, page_hi = pages.split("-")
    else:
        page_lo, page_hi = None, None

    edit_form = RefEditForm(
        pages_lo=page_lo,
        pages_hi=page_hi,
        **ref.__dict__
    )

    return flask.render_template('ref.html', title="Edit Ref",
                                 ref=ref, edit_form=edit_form)


@refs.route('/ref/<ref_id>', methods=['POST'])
@login_required
def ref_post(ref_id):
    form = RefEditForm()

    ref = Ref.query.filter_by(
        user_id=current_user.id,
        id=ref_id
    ).first_or_404()

    if form.validate_on_submit():
        ref = ref_model_updater(ref, form)
        db.session.commit()
        ref_url = flask.url_for('refs.index')

        flask.flash(flask.Markup(
            f"Reference updated. <a href=\"{ref_url}\">Go back to Refs</a>"
        ))

    # return flask.redirect(flask.url_for('refs.ref', ref_id=ref_id, edit_form=form))
    return flask.render_template('ref.html', title="Edit ref", ref=ref, edit_form=form)


@refs.route('/refs/upload/', methods=['POST'])
@login_required
def upload_bib_file():
    form = UploadBibFileForm()

    if form.validate_on_submit():
        parser = BibTexMagic()

        parser.parse_bib(form.filename.data)

        for entry in parser.entries:
            try:
                ref = ref_model_factory_from_dict(entry.entry_type, entry.to_dict())
                ref.owner = current_user
                db.session.add(ref)
            except ValueError:
                flask.flash(f"Warning: Entry type '{entry.entry_type}'" + \
                            f"is not supported.")

        db.session.commit()


    return flask.redirect(flask.url_for('refs.index'))

@refs.route('/refs/delete/', methods=['DELETE'])
@login_required
def delete():
    to_del = [int(entry[len('selected_'):]) for entry in flask.request.form]

    del_count = Ref.query.filter(
        Ref.user_id==current_user.id,
        Ref.id.in_(to_del)
    ).delete(synchronize_session='fetch')

    db.session.commit()

    if del_count == 0:
        flask.flash("No Refs were deleted.")
    elif del_count == 1:
        flask.flash(f"Succesfully deleted {del_count} Ref.")
    else:
        flask.flash(f"Succesfully deleted {del_count} Refs.")


    return flask.jsonify(del_count=del_count)