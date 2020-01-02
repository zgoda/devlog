import os

from flask import (
    Response, abort, current_app, flash, redirect, render_template, request, url_for,
)
from flask_babel import lazy_gettext as gettext
from flask_login import current_user, login_required

from ..ext import db
from ..models import Blog
from ..post.service import get_recent as recent_posts
from ..utils.forms import Button, DeleteForm
from ..utils.pagination import paginate
from ..utils.views import path_for_file_upload, valid_files
from . import blog_bp
from .forms import BlogForm, PostImportForm
from .service import get_default


@blog_bp.route('/create', methods=['POST', 'GET'])
@login_required
def create() -> Response:
    if not current_user.active:
        flash(gettext('your account is inactive'), category='warning')
        return redirect(url_for('user.account'))
    form = BlogForm()
    if form.validate_on_submit():
        blog = form.save(save=False)
        blog.default = get_default() is None
        db.session.add(blog)
        db.session.commit()
        flash(
            gettext('Your blog %(name)s has been created', name=blog.name),
            category='success',
        )
        return redirect(url_for('.display', blog_id=blog.id))
    context = {
        'form': form,
    }
    return render_template('blog/create.html', **context)


@blog_bp.route('/<int:blog_id>')
def display(blog_id: int) -> Response:
    blog = Blog.query.get_or_404(blog_id)
    if not blog.active and (current_user != blog.user):
        abort(404)
    active_only = (current_user != blog.user)
    query = recent_posts(blog=blog, active_only=active_only)
    pagination = paginate(query, size=10)
    context = {
        'blog': blog,
        'posts': pagination,
    }
    return render_template('blog/display.html', **context)


@blog_bp.route('/<int:blog_id>/details', methods=['POST', 'GET'])
@login_required
def details(blog_id: int) -> Response:
    blog = Blog.query.get_or_404(blog_id)
    if current_user != blog.user:
        abort(404)
    form = None
    if request.method == 'POST':
        form = BlogForm()
        if form.validate_on_submit():
            form.save(obj=blog)
            flash(
                gettext('blog %(name)s has been modified', name=blog.name),
                category='success',
            )
            return redirect(url_for('.display', blog_id=blog.id))
    context = {
        'blog': blog,
        'form': form or BlogForm(obj=blog),
        'import_form': PostImportForm(),
    }
    return render_template('blog/details.html', **context)


@blog_bp.route('/<int:blog_id>/contentimport', methods=['POST', 'GET'])
@login_required
def import_posts(blog_id: int) -> Response:
    blog = Blog.query.get_or_404(blog_id)
    if blog.user != current_user:
        abort(403)
    if request.method == 'POST':
        final = redirect(url_for('blog.details', blog_id=blog_id))
        if 'files' not in request.files:
            flash(gettext('no files uploaded'), category='warning')
            return final
        valid_uploads = valid_files(request.files.getlist('files'))
        if not valid_uploads:
            flash(gettext('no valid files uploaded'), category='warning')
            return final
        for fs in valid_uploads:
            file_path = path_for_file_upload(fs)
            fs.save(file_path)
            queue = current_app.queues['tasks']
            queue.enqueue('devlog.tasks.import_post', file_path, blog_id)
            flash(
                gettext(
                    'import of post file %(file_name)s has been scheduled',
                    file_name=os.path.split(file_path)[-1],
                ),
                category='success'
            )
        return final
    ctx = {
        'blog': blog,
        'form': PostImportForm()
    }
    return render_template('blog/import.html', **ctx)


@blog_bp.route('/<int:blog_id>/delete', methods=['POST', 'GET'])
@login_required
def delete(blog_id: int) -> Response:
    blog = Blog.query.get_or_404(blog_id)
    if current_user != blog.user:
        abort(404)
    form = DeleteForm()
    if form.validate_on_submit() and form.confirm():
        blog_name = blog.name
        db.session.delete(blog)
        db.session.commit()
        flash(
            gettext(
                'your blog %(blog_name)s has been completely removed from the site',
                blog_name=blog_name,
            ),
            category='success',
        )
        return redirect('home.index')
    form.buttons = [
        Button(class_='danger', icon='skull-crossbones', text=gettext('confirm'))
    ]
    context = {
        'form': form,
        'blog': blog,
    }
    return render_template('blog/delete.html', **context)
