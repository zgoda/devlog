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
        user = form.login()
        if user:
            if not user.otp_registered:
                flash('Prawidłowe dane logowania', category='success')
                return redirect(url_for('auth.mfa-qrcode'))
            flash('Użytkownk ma już sparowaną aplikację OTP', category='warning')
            del session['user']
            return redirect(url_for('auth.login'))
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
        del session['user']
    form = OTPCodeForm()
    if form.validate_on_submit():
        if form.verify(user):
            login_user(user)
            session.permanent = True
            user.register_otp()
            flash('Użytkownik zalogowany', category='success')
            return redirect(next_redirect('main.index'))
        flash('Podany kod jest nieprawidłowy, spróbuj jeszcze raz', category='warning')
        return redirect(url_for('auth.mfa-begin'))
    return render_template('auth/qrcode.html', form=form), 200, NO_CACHE_HEADERS


@bp.route('/qrcode', endpoint='mfa-qrcode-gen')
def mfa_qrcode_gen():
    if 'user' not in session:
        abort(404)
    name = session['user']
    user = User.get_or_none(User.name == name)
    if user is None:
        del session['user']
        abort(404)
    data = user.provisioning_uri
    headers = NO_CACHE_HEADERS.copy()
    headers['Content-Type'] = 'image/svg+xml'
    image = qrcode.make(data, image_factory=qrcode.image.svg.SvgPathFillImage)
    with io.BytesIO() as stream:
        image.save(stream)
        return stream.getvalue(), 200, headers


@bp.route('/logout', methods=['POST', 'GET'])
@login_required
def logout():  # pragma: nocover
    logout_user()
    flash('Użytkownik wylogowany')
    return redirect(url_for('main.index'))
