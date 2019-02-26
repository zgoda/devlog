from flask import render_template, request

from . import auth_bp


@auth_bp.route('/select')
def select():
    return render_template('auth/select.html')


@auth_bp.route('/<provider>/login')
def login(provider):
    if provider == 'local':
        return local_login_callback(request.args.get('email'))


def local_login_callback():
    pass
