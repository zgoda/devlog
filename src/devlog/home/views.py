from flask import Response, current_app, render_template
from flask_login import current_user

from ..blog.service import get_recent as recent_blogs
from ..post.service import get_by_ident, get_recent as recent_posts
from ..post.views import post_display_func
from . import home_bp


@home_bp.route('/')
def index() -> Response:
    kw = {
        'limit': current_app.config.get('SHORT_LIST_LIMIT', 5),
    }
    if current_user.is_authenticated:
        kw['extra_user'] = current_user
    blogs = recent_blogs(**kw)
    posts = recent_posts(**kw)
    context = {
        'blogs': blogs,
        'posts': posts,
    }
    return render_template('index.html', **context)


@home_bp.route('/<int:y>/<int:m>/<int:d>/<slug>', endpoint='post')
def display_single_post(y: int, m: int, d: int, slug: str) -> Response:
    post = get_by_ident(y, m, d, slug)
    return post_display_func(post)
