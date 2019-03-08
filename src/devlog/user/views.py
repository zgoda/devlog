from flask import flash, redirect, render_template, request
from flask_babel import lazy_gettext as gettext
from flask_login import login_required, current_user

from . import user_bp
from .forms import UserForm
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


@user_bp.route('/deactivate')
@login_required
def deactivate():
    pass


@user_bp.route('/delete')
@login_required
def delete():
    pass
