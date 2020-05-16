from typing import Union

from flask import Response, flash, redirect, render_template, request
from flask_babel import get_locale, lazy_gettext
from flask_login import current_user, login_required

from ..utils.i18n import localized_timezone_choices
from . import user_bp
from .forms import UserForm


@user_bp.route('/account', methods=['POST', 'GET'])
@login_required
def account() -> Union[str, Response]:
    form = None
    if request.method == 'POST':
        form = UserForm()
        if form.validate_on_submit():
            user = form.save(current_user)
            flash(
                lazy_gettext(
                    'user %(name)s details have been saved', name=user.name
                ),
                category='success',
            )
            return redirect(request.path)
    if form is None:
        form = UserForm(obj=current_user)
        form.timezone.choices = localized_timezone_choices(get_locale())
    context = {
        'form': form,
    }
    return render_template('user/details.html', **context)
