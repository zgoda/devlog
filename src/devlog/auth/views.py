import io

import qrcode
import qrcode.image.svg
from flask import abort, flash, redirect, render_template, request, session, url_for
from flask_login import login_required, login_user, logout_user

from ..models import User
from ..utils.views import next_redirect
from ..utils.web import NO_CACHE_HEADERS
from . import auth_bp as bp
from .forms import LoginForm, OTPCodeForm, PartialLoginForm


@bp.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.login():
            flash('Użytkownik zalogowany', category='success')
        else:
            flash('Nieprawidłowe dane logowania', category='danger')
        return redirect(next_redirect('main.index'))
    return render_template('auth/login.html', form=form)


@bp.route('/2fa', endpoint='mfa-begin', methods=['POST', 'GET'])
def mfa_begin():
    form = PartialLoginForm()
    if form.validate_on_submit():
        if form.login():
            flash('Prawidłowe dane logowania', category='success')
            return redirect(url_for('auth.mfa-qrcode'))
        flash('Nieprawidłowe dane logowania', category='warning')
    return render_template('auth/login.html', form=form, partial=True)


@bp.route('/pair', endpoint='mfa-qrcode', methods=['POST', 'GET'])
def mfa_qrcode():
    login_redirect = redirect(url_for('auth.login'))
    if 'user' not in session:
        return login_redirect
    name = session['user']
    user = User.get_or_none(User.name == name)
    if user is None:
        return login_redirect
    if request.method == 'POST':
        session.pop('user', None)
    form = OTPCodeForm()
    if form.validate_on_submit():
        if form.verify(user):
            login_user(user)
            session.permanent = True
            user.register_otp(True)
            flash('Użytkownik zalogowany', category='success')
            return redirect(next_redirect('main.index'))
    return render_template('auth/qrcode.html', form=form), 200, NO_CACHE_HEADERS


@bp.route('/qrcode', endpoint='mfa-qrcode-gen')
def mfa_qrcode_gen():
    if 'user' not in session:
        abort(404)
    name = session['user']
    user = User.get_or_none(User.name == name)
    data = user.provisioning_uri
    headers = NO_CACHE_HEADERS.copy()
    headers['Content-Type'] = 'image/svg+xml'
    image = qrcode.make(data, image_factory=qrcode.image.svg.SvgPathFillImage)
    with io.BytesIO() as stream:
        image.save(stream)
        return stream.getvalue(), 200, headers


@bp.route('/logout', methods=['POST', 'GET'])
@login_required
def logout():
    logout_user()
    flash('Użytkownik wylogowany')
    return redirect(url_for('main.index'))
