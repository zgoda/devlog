from flask import session, flash, redirect
from flask_babel import lazy_gettext as gettext
from flask_login import login_user

from ..ext import db
from ..models import User
from ..utils.views import next_redirect


def login_success(email, access_token, remote_id, service, **kwargs):
    if email is None:
        user = User.get_by_remote_auth(service, remote_id)
        ident = kwargs.get('name')
    else:
        user = User.get_by_email(email)
        ident = email
    if user is None:
        user = User(email=email, remote_user_id=remote_id, oauth_service=service)
    user.access_token = access_token
    kwargs.pop('id', None)
    for k, v in kwargs.items():
        setattr(user, k, v)
    db.session.add(user)
    db.session.commit()
    login_user(user)
    session.permanent = True
    flash(
        gettext(
            'you have been signed in as %(ident)s using %(service)s',
            ident=ident, service=service
        ), category='success'
    )
    return redirect(next_redirect('home.index'))
