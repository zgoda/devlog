from flask import abort, flash, redirect, render_template, request, url_for
from flask_babel import lazy_gettext as gettext
from flask_login import current_user, login_required

from . import post_bp
from ..models import Blog, Post
from .forms import PostForm


@post_bp.route('/inblog/<int:blog_id>', methods=['POST', 'GET'])
@login_required
def create(blog_id):
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
    return render_template('post/create.jinja', **context)


@post_bp.route('/<int:post_id>', methods=['POST', 'GET'], defaults={'slug': None})
@post_bp.route('/<int:post_id>/<slug>', methods=['POST', 'GET'])
def display(post_id, slug):
    post = Post.query.get_or_404(post_id)
    if (not post.public or post.draft) and current_user != post.blog.user:
        abort(404)
    form = None
    if request.method == 'POST':
        form = PostForm()
        if form.validate_on_submit():
            form.save(post.blog, obj=post)
            flash(gettext('your blog post has been saved'), category='success')
            return redirect(request.path)
    context = {
        'post': post,
        'form': form or PostForm(obj=post),
    }
    return render_template('post/display.jinja', **context)
