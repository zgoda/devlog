from typing import Union

from flask import Response, abort, flash, redirect, render_template, request, url_for
from flask_babel import lazy_gettext as gettext
from flask_login import current_user, login_required

from ..models import Blog, Post
from . import post_bp, service
from .forms import PostForm
from ..utils.pagination import paginate


@post_bp.route('/inblog/<int:blog_id>', methods=['POST', 'GET'])
@login_required
def create(blog_id: int) -> Union[str, Response]:
    blog = Blog.query.get_or_404(blog_id)
    if blog.user != current_user:
        abort(404)
    form = None
    if request.method == 'POST':
        form = PostForm()
        if form.validate_on_submit():
            form.save(blog)
            flash(gettext('your blog post has been saved'), category='success')
            return redirect(url_for('blog.display', blog_id=blog.id))
    context = {
        'blog': blog,
        'form': form or PostForm(),
    }
    return render_template('post/create.html', **context)


def post_display_func(post: Post) -> Union[str, Response]:
    if post.draft and current_user != post.blog.user:
        abort(404)
    form = None
    if request.method == 'POST':
        if current_user != post.blog.user:
            abort(404)
        form = PostForm()
        if form.validate_on_submit():
            form.save(post.blog, obj=post)
            flash(gettext('your blog post has been saved'), category='success')
            return redirect(request.path)
    context = {
        'post': post,
        'form': form or PostForm(obj=post),
    }
    return render_template('post/display.html', **context)


@post_bp.route('/<int:post_id>', methods=['POST', 'GET'])
def display(post_id: int) -> Union[str, Response]:
    post = Post.query.get_or_404(post_id)
    return post_display_func(post)


@post_bp.route('/recent')
def recent() -> str:
    active_only = not current_user.is_authenticated
    query = service.get_recent(active_only=active_only)
    ctx = {
        'pagination': paginate(query),
    }
    return render_template('post/list.html', **ctx)
