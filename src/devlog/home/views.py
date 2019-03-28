from flask import render_template, current_app
from flask_login import current_user

from . import home_bp
from ..blog.service import get_recent as recent_blogs
from ..post.service import get_recent as recent_posts


@home_bp.route('/')
def index():
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
    return render_template('index.jinja', **context)
