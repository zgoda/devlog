from flask import flash, redirect, render_template

from ..utils.views import next_redirect
from . import auth_bp as bp
from .forms import LoginForm


@bp.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.login():
            flash('Użytkownik zalogowany', category='success')
            return redirect(next_redirect('main.index'))
    return render_template('auth/login.html', form=form)
