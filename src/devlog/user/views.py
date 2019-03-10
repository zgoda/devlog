from flask import flash, redirect, render_template, request, url_for
from flask_babel import lazy_gettext as gettext
from flask_login import login_required, current_user, logout_user

from . import user_bp
from .forms import UserForm
from ..ext import db
from ..utils.forms import DeleteForm


@user_bp.route('', methods=['POST', 'GET'])
@login_required
def profile():
    form = None
    if request.method == 'POST':
        form = UserForm()
        if form.validate_on_submit():
            form.save(current_user)
            flash(
                gettext(
                    'Data for user %(name)s has been saved',
                    name=current_user.display_name()
                ), category='success'
            )
            return redirect(request.path)
    context = {
        'form': form or UserForm(obj=current_user)
    }
    return render_template('user/details.jinja', **context)


@user_bp.route('/remove')
@login_required
def deactivate_or_delete():
    context = {
        'deactivation_form': DeleteForm(),
        'delete_form': DeleteForm()
    }
    return render_template('user/remove.jinja', **context)


@user_bp.route('/deactivate', methods=['POST'])
@login_required
def deactivate():
    form = DeleteForm()
    if form.confirm():
        current_user.active = False
        db.session.add(current_user)
        db.session.commit()
        flash(gettext('Account deactivated'), category='success')
    return redirect(url_for('.profile'))


@user_bp.route('/delete', methods=['POST'])
@login_required
def delete():
    form = DeleteForm()
    if form.confirm():
        user_name = current_user.name or current_user.email or gettext('no name')
        logout_user()
        db.session.delete(current_user)
        db.session.commit()
        flash(gettext('Account for user %(name)s deleted', name=user_name), category='success')
        return redirect(url_for('home.index'))
    return redirect(url_for('.profile'))
