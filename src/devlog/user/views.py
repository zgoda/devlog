from flask import (
    Response, abort, current_app, flash, redirect, render_template, request, url_for,
)
from flask_babel import get_locale, gettext, lazy_gettext
from flask_login import current_user, login_required, logout_user

from ..ext import db
from ..models import User
from ..utils.forms import DeleteForm
from ..utils.i18n import localized_timezone_choices
from . import user_bp
from .forms import UserForm
from .utils import check_token, generate_token


@user_bp.route('/account', methods=['POST', 'GET'])
@login_required
def account() -> Response:
    form = None
    if request.method == 'POST':
        old_email = current_user.email
        was_confirmed = current_user.email_confirmed
        form = UserForm()
        if form.validate_on_submit():
            user = form.save(current_user)
            flash(
                lazy_gettext(
                    'user %(email)s details have been saved', email=user.email
                ),
                category='success',
            )
            if old_email != user.email and was_confirmed:
                flash(
                    lazy_gettext(
                        'email address has been changed, '
                        'new email will have to be confirmed again'
                    ),
                    category='warning'
                )
            return redirect(request.path)
    if form is None:
        form = UserForm(obj=current_user)
        form.timezone.choices = localized_timezone_choices(get_locale())
    context = {
        'form': form,
    }
    return render_template('user/details.html', **context)


@user_bp.route('/confirmation/start')
@login_required
def confirmation_start() -> Response:
    return render_template('user/confirmation_start.html')


@user_bp.route('/confirmation/send', methods=['POST'])
@login_required
def confirmation_send() -> Response:
    token = generate_token(current_user.email)
    confirmation_url = url_for('user.confirmation_finish', token=token, _external=True)
    html = render_template(
        'user/email/confirmation.html', confirmation_url=confirmation_url
    )
    queue = current_app.queues['mail']
    queue.enqueue(
        'devlog.tasks.send_email', [current_user.email],
        gettext('Devlog email confirmation'), html,
    )
    flash(
        lazy_gettext(
            'confirmation email has been sent to your email address, '
            'please check your mailbox'
        ),
        category='success'
    )
    return redirect(url_for('user.account'))


@user_bp.route('/confirmation/finish/<token>')
def confirmation_finish(token: str) -> Response:
    fail_target = redirect(url_for('home.index'))
    success, result = check_token(token)
    if success:
        user = User.get_by_email(result)
        if user is None:
            flash(
                lazy_gettext('user %(email)s not found', email=result),
                category='danger',
            )
            return fail_target
        user.confirm_email()
        db.session.add(user)
        db.session.commit()
        flash(
            lazy_gettext('your email has been succesfully confirmed'),
            category='success',
        )
        return redirect(url_for('user.account'))
    else:
        if result == 'expired':
            msg = lazy_gettext(
                'the token has expired, please start new confirmation process again'
            )
        elif result == 'invalid':
            msg = lazy_gettext('the token is invalid')
        else:
            msg = lazy_gettext('token check failed')
        flash(msg, category='danger')
        return fail_target


@user_bp.route('/<int:user_id>')
@login_required
def profile(user_id: int) -> Response:
    user = User.query.get_or_404(user_id)
    if user != current_user and not (user.public and user.active):
        abort(404)
    context = {
        'user': user,
    }
    return render_template('user/profile.html', **context)


@user_bp.route('/confirmation/remove', methods=['POST', 'GET'])
@login_required
def confirmation_remove():
    form = DeleteForm()
    if form.validate_on_submit():
        confirmed = form.confirm()
        if confirmed:
            current_user.clear_email_confirmation()
            db.session.add(current_user)
            db.session.commit()
            flash(
                lazy_gettext('your email is now unconfirmed again'), category='warning'
            )
        return redirect(url_for('user.account'))
    ctx = {
        'form': form,
    }
    return render_template('user/confirmation_remove.html', **ctx)


@user_bp.route('/remove')
@login_required
def confirm_delete() -> Response:
    context = {
        'delete_form': DeleteForm(),
    }
    return render_template('user/remove.html', **context)


@user_bp.route('/delete', methods=['POST'])
@login_required
def delete() -> Response:
    form = DeleteForm()
    if form.confirm():
        user_name = current_user.name or current_user.email or lazy_gettext('no name')
        db.session.delete(current_user)
        db.session.commit()
        logout_user()
        flash(
            lazy_gettext('Account for user %(name)s deleted', name=user_name),
            category='success',
        )
        return redirect(url_for('home.index'))
    return redirect(url_for('.account'))
