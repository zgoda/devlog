from flask import Response, flash, redirect, render_template, request
from flask_babel import lazy_gettext as gettext
from flask_login import login_required, logout_user

from ..utils.views import next_redirect
from . import auth_bp
from .forms import LoginForm, RegisterForm
from .utils import login_success


@auth_bp.route('/register', methods=['POST', 'GET'])
def register() -> Response:
    logout_user()
    form = RegisterForm()
    if form.validate_on_submit():
        user = form.save()
        login_success(user)
        flash(
            gettext(
                f'account for {user.email} has been registered, you are now logged in'
            ),
            category='success',
        )
        return redirect(next_redirect('home.index'))
    ctx = {
        'form': form,
    }
    return render_template('auth/register.html', **ctx)


@auth_bp.route('/login', methods=['POST', 'GET'])
def login() -> Response:
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
        login_success(user)
        flash(gettext(f'user {user.email} logged in'), category='success')
        return redirect(next_redirect('home.index'))
    ctx = {
        'form': form,
    }
    return render_template('auth/login.html', **ctx)


@auth_bp.route('/logout')
@login_required
def logout() -> Response:
    logout_user()
    return redirect(next_redirect('home.index'))
