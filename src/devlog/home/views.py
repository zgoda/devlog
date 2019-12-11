from flask import Response, current_app, render_template
from flask_login import current_user

from ..blog.service import get_recent as recent_blogs
from ..post.service import get_recent as recent_posts
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
