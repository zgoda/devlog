from flask import abort, flash, redirect, render_template, request, url_for
from flask_babel import lazy_gettext as gettext
from flask_login import current_user, login_required

from . import blog_bp
from ..ext import db
from ..models import Blog, Post
from ..utils.pagination import get_page
from .forms import BlogForm


@blog_bp.route('/create', methods=['POST', 'GET'])
@login_required
def create():
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
    return render_template('blog/create.jinja', **context)


@blog_bp.route('/<int:blog_id>')
def display(blog_id):
    blog = Blog.query.get_or_404(blog_id)
    if not (blog.active and blog.public) and (current_user != blog.user):
        abort(404)
    page = get_page()
    query = blog.posts
    if (current_user != blog.user):
        query = query.filter(Post.public.is_(True), Post.published.isnot(None))
    pagination = query.order_by(db.desc(Post.updated)).paginate(page, 10)
    context = {
        'blog': blog,
        'posts': pagination,
    }
    return render_template('blog/display.jinja', **context)


@blog_bp.route('/<int:blog_id>/details', methods=['POST', 'GET'])
@login_required
def details(blog_id):
    blog = Blog.query.get_or_404(blog_id)
    if current_user != blog.user:
        abort(404)
    form = None
    if request.method == 'POST':
        form = BlogForm()
        if form.validate_on_submit():
            form.save(obj=blog)
            flash(gettext('blog %(name)s has been modified', name=blog.name), category='success')
            return redirect(url_for('.display', blog_id=blog.id))
    context = {
        'blog': blog,
        'form': form or BlogForm(obj=blog),
    }
    return render_template('blog/details.jinja', **context)
