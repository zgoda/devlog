import os
from typing import Optional

from flask import (
    Response, abort, current_app, flash, redirect, render_template, request, url_for,
)
from flask_babel import lazy_gettext as gettext
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename

from ..ext import db
from ..models import Blog, Post
from ..post.service import get_recent as recent_posts
from ..utils.forms import Button, DeleteForm
from ..utils.pagination import get_page
from . import blog_bp
from .forms import BlogForm, PostImportForm


@blog_bp.route('/create', methods=['POST', 'GET'])
@login_required
def create() -> Response:
    if not current_user.active:
        flash(gettext('your account is inactive'), category='warning')
        return redirect(url_for('user.account'))
    form = None
    if request.method == 'POST':
        form = BlogForm()
        if form.validate_on_submit():
            blog = form.save()
            flash(
                gettext('Your blog %(name)s has been created', name=blog.name),
                category='success',
            )
            return redirect(url_for('.display', blog_id=blog.id))
    context = {
        'form': form or BlogForm(),
    }
    return render_template('blog/create.html', **context)


@blog_bp.route('/<int:blog_id>', defaults={'slug': None})
@blog_bp.route('/<int:blog_id>/<slug>')
def display(blog_id: int, slug: Optional[str]) -> Response:
    blog = Blog.query.get_or_404(blog_id)
    if not (blog.active and blog.public) and (current_user != blog.user):
        abort(404)
    page = get_page()
    public_only = True
    with_drafts = False
    extra_user = None
    if current_user == blog.user:
        public_only = False
        with_drafts = True
        extra_user = blog.user
    query = recent_posts(
        blog=blog, public_only=public_only, drafts=with_drafts,
        extra_user=extra_user,
    )
    pagination = query.order_by(db.desc(Post.updated)).paginate(page, 10)
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


@blog_bp.route('/<int:blog_id>/contentimport', methods=['POST'])
@login_required
def import_posts(blog_id: int) -> Response:
    final = redirect(url_for('.details', blog_id=blog_id))
    if 'files' not in request.files:
        flash(gettext('no files uploaded'), category='warning')
        return final
    file_storages = request.files.getlist('files')
    valid_files = []
    for fs in file_storages:
        if fs.filename != '' and \
                fs.filename.endswith(current_app.config['ALLOWED_UPLOAD_EXTENSIONS']):
            valid_files.append(fs)
    if not valid_files:
        flash(gettext('no valid files uploaded'), category='warning')
        return final
    for fs in valid_files:
        file_name = secure_filename(fs.filename)
        upload_dir = os.path.join(
            current_app.instance_path, current_app.config['UPLOAD_DIR_NAME']
        )
        file_path = os.path.join(upload_dir, file_name)
        fs.save(file_path)
        current_app.task_queue.enqueue('devlog.tasks.import_post', file_path, blog_id)
        flash(
            gettext(
                'import of post file %(file_name)s has been scheduled',
                file_name=file_name,
            ),
            category='success'
        )
    return final


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
