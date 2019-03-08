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


@user_bp.route('/remove', methods=['POST', 'GET'])
@login_required
def remove():
    deactivation_form = delete_form = None
    context = {
        'deactivation_form': deactivation_form or DeleteForm(),
        'delete_form': delete_form or DeleteForm()
    }
    return render_template('user/remove.jinja', **context)
