from flask import render_template, request, flash, redirect, url_for, session
from flask_babel import lazy_gettext as gettext

from ..ext import oauth
from . import auth_bp
from . import provider as providers
from .utils import login_success


@auth_bp.route('/select')
def select():
    return render_template('auth/select.html')


@auth_bp.route('/<provider>/login')
def login(provider):
    if provider == 'local':
        return local_login_callback(request.args.get('email'))
    service = getattr(providers, provider, None)
    if service is None:
        flash(
            gettext(
                'service %(provider)s is not supported', provider=provider
            ), category='danger'
        )
        return redirect(url_for('.select'))
    endpoint = '.callback-{}'.format(provider)
    callback = url_for(endpoint, _external=True)
    return service.authorize_redirect(callback)


@auth_bp.route('/local/callback', endpoint='callback-local')
def local_login_callback(email):
    return login_success(email, 'local', 'local', 'local handler')


@auth_bp.route('/github/callback', endpoint='callback-github')
def github_login_callback():
    token_data = oauth.github.authorize_access_token()
    if token_data:
        access_token = token_data.get('access_token')
        session['access_token'] = token_data, ''
        resp = oauth.github.get('/user')
        if resp.ok:
            user_data = resp.json()
            email = user_data.pop('email', None)
            return login_success(
                email, access_token, user_data['id'], 'github', **user_data,
            )
    return redirect(url_for('.select'))
