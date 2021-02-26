from flask import flash, redirect, render_template

from ..utils.views import next_redirect
from . import auth_bp as bp
from .forms import CodeForm, CodeLoginForm, LoginForm


@bp.route('/login', methods=['POST', 'GET'])
def login():
    form = CodeLoginForm()
    if form.validate_on_submit():
        if form.login():
            flash('Użytkownik zalogowany', category='success')
            return redirect(next_redirect('main.index'))
    return render_template('auth/login.html', form=form)


@bp.route('/register', endpoint='qrcode-login', methods=['POST', 'GET'])
def qrcode1():
    form = LoginForm()
    return render_template('auth/register.html', form=form)


@bp.route('/code', endpoint='qrcode-code', methods=['POST', 'GET'])
def qrcode2():
    form = CodeForm()
    return render_template('auth/code.html', form=form)
