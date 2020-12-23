from flask import abort, render_template

from ..models import User
from . import activitypub_bp as bp


@bp.route('/ap/<name>/profile')
def userprofile(name: str):
    user = User.get_or_none(User.name == name)
    if not user:
        abort(404)
    return render_template('ap/userprofile.html', user=user)
