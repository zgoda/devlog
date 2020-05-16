from typing import Union

from flask import Response, flash, redirect, render_template, request, session
from flask_babel import lazy_gettext as gettext
from flask_login import current_user, login_required, login_user, logout_user

from ..utils.views import next_redirect
from . import auth_bp
from .forms import LoginForm


@auth_bp.route('/login', methods=['POST', 'GET'])
def login() -> Union[str, Response]:
    logout_user()
    form = LoginForm()
    if form.validate_on_submit():
        user = form.login()
        if user is None:
            flash(
                gettext(
                    'login failed, either user is not known or password is incorrect'
                ),
                category='danger'
            )
            return redirect(request.path)
        login_user(user)
        session.permanent = True
        flash(gettext('user %(name)s logged in', name=user.name), category='success')
        return redirect(next_redirect('home.index'))
    ctx = {
        'form': form,
    }
    return render_template('auth/login.html', **ctx)


@auth_bp.route('/logout')
@login_required
def logout() -> Response:
    user_name = current_user.name
    logout_user()
    flash(gettext('user %(user)s signed out', user=user_name), category='success')
    return redirect(next_redirect('home.index'))
