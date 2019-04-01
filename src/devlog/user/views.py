from flask import abort, flash, redirect, render_template, request, url_for
from flask_babel import get_locale
from flask_babel import lazy_gettext as gettext
from flask_login import current_user, login_required, logout_user

from . import user_bp
from ..ext import db
from ..models import User
from ..utils.forms import DeleteForm
from ..utils.i18n import localized_timezone_choices
from .forms import UserForm


@user_bp.route('', methods=['POST', 'GET'])
@login_required
def account():
    form = None
    if request.method == 'POST':
        form = UserForm()
        if form.validate_on_submit():
            form.save(current_user)
            flash(
                gettext(
                    'Data for user %(name)s has been saved', name=current_user.name
                ),
                category='success',
            )
            return redirect(request.path)
    if form is None:
        form = UserForm(obj=current_user)
    form.timezone.choices = localized_timezone_choices(get_locale())
    context = {
        'form': form or UserForm(obj=current_user),
    }
    return render_template('user/details.jinja', **context)


@user_bp.route('/<int:user_id>')
@login_required
def profile(user_id):
    user = User.query.get_or_404(user_id)
    if user != current_user and not (user.public and user.active):
        abort(404)
    context = {
        'user': user,
    }
    return render_template('user/profile.jinja', **context)


@user_bp.route('/remove')
@login_required
def confirm_delete():
    context = {
        'delete_form': DeleteForm(),
    }
    return render_template('user/remove.jinja', **context)


@user_bp.route('/delete', methods=['POST'])
@login_required
def delete():
    form = DeleteForm()
    if form.confirm():
        user_name = current_user.name or current_user.email or gettext('no name')
        db.session.delete(current_user)
        db.session.commit()
        logout_user()
        flash(
            gettext('Account for user %(name)s deleted', name=user_name),
            category='success',
        )
        return redirect(url_for('home.index'))
    return redirect(url_for('.account'))
