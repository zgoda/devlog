from flask import flash, redirect, render_template, request
from flask_babel import lazy_gettext as gettext
from flask_login import login_required

from . import user_bp
from ..models import User
from .forms import UserForm


@user_bp.route('/<int:user_id>', methods=['POST', 'GET'])
@login_required
def details(user_id):
    user = User.query.get_or_404(user_id)
    form = None
    if request.method == 'POST':
        form = UserForm()
        if form.validate_on_submit():
            user = form.save(user)
            flash(
                gettext(
                    'Data for user %(name)s has been saved', name=user.display_name()
                ), category='success'
            )
            return redirect(request.path)
    context = {
        'user': user,
        'form': form or UserForm(obj=user)
    }
    return render_template('user/details.html', **context)
