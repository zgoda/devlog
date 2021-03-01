import io
import qrcode
import qrcode.image.svg
from flask import abort, flash, redirect, render_template, session, url_for, request
from flask_login import login_user

from ..utils.views import next_redirect
from . import auth_bp as bp
from .forms import LoginForm, OTPCodeForm, PartialLoginForm
from ..models import User


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
            return redirect(url_for('auth.mfa-qrcode'))
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
            return redirect(next_redirect('main.index'))
    headers = {
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0',
    }
    return render_template('auth/qrcode.html', form=form), 200, headers


@bp.route('/qrcode', endpoint='mfa-qrcode-gen')
def mfa_qrcode_gen():
    if 'user' not in session:
        abort(404)
    name = session['user']
    user = User.get_or_none(User.name == name)
    data = user.provisioning_uri
    factory = qrcode.image.svg.SvgPathFillImage
    image = qrcode.make(data, image_factory=factory)
    stream = io.BytesIO()
    image.save(stream)
    headers = {
        'Content-Type': 'image/svg+xml',
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0',
    }
    return stream.getvalue(), 200, headers
