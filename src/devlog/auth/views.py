from flask import flash, redirect, render_template, request, session, url_for
from flask_babel import lazy_gettext as gettext
from flask_login import login_required, logout_user

from . import auth_bp
from . import provider as providers
from ..ext import oauth
from ..utils.views import next_redirect
from .utils import login_success


@auth_bp.route('/select')
def select():
    return render_template('auth/select.jinja')


@auth_bp.route('/<provider>/login')
def login(provider):  # pragma: nocover
    if provider == 'local':
        return local_login_callback(request.args.get('email'))
    service = getattr(providers, provider, None)
    if service is None:
        flash(
            gettext('service %(provider)s is not supported', provider=provider),
            category='danger',
        )
        return redirect(url_for('.select'))
    endpoint = f'.callback-{provider}'
    callback = url_for(endpoint, _external=True)
    return service.authorize_redirect(callback)


@auth_bp.route('/local/callback', endpoint='callback-local')
def local_login_callback(email):
    name = request.args.get('name', 'example user')
    return login_success(email, 'local', 'local', 'local handler', name=name)


@auth_bp.route('/facebook/callback', endpoint='callback-facebook')
def facebook_login_callback():  # pragma: nocover
    token_data = oauth.facebook.authorize_access_token()
    if token_data:
        access_token = token_data.get('access_token')
        session['access_token'] = token_data, ''
        resp = oauth.facebook.get(
            '/me', params={'fields': 'id,email,first_name,last_name'}
        )
        if resp.ok:
            user_data = resp.json()
            email = user_data.get('email')
            first_name = user_data.get('first_name', '')
            last_name = user_data.get('last_name', '')
            name = f'{first_name} {last_name}'.strip()
            return login_success(
                email, access_token, user_data['id'], 'facebook', name=name,
            )
    return redirect(url_for('.select'))


@auth_bp.route('/google/callback', endpoint='callback-google')
def google_login_callback():  # pragma: nocover
    token_data = oauth.google.authorize_access_token()
    if token_data:
        access_token = token_data.get('access_token')
        session['access_token'] = token_data, ''
        resp = oauth.google.get('/oauth2/v3/userinfo')
        if resp.ok:
            user_data = resp.json()
            email = user_data.pop('email', None)
            user_id = user_data.pop('sub', None)
            return login_success(
                email, access_token, user_id, 'google', **user_data,
            )
    return redirect(url_for('.select'))


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(next_redirect('home.index'))
