from flask import Response, current_app, render_template
from flask_login import current_user

from ..blog.service import get_default, get_recent as recent_blogs
from ..post.service import get_by_ident, get_recent as recent_posts
from ..post.views import post_display_func
from . import home_bp
from ..utils.pagination import paginate


@home_bp.route('/')
def index() -> Response:
    limit = current_app.config.get('SHORT_LIST_LIMIT', 5)
    active_only = not current_user.is_authenticated
    blog = get_default()
    posts_query = recent_posts(active_only=active_only, blog=blog)
    context = {
        'recent_blogs': recent_blogs(active_only=active_only),
        'recent_posts': recent_posts(active_only=active_only, limit=limit),
        'blog': blog,
        'posts': paginate(posts_query),
    }
    return render_template('index.html', **context)


@home_bp.route('/<int:y>/<int:m>/<int:d>/<slug>', endpoint='post')
def display_single_post(y: int, m: int, d: int, slug: str) -> Response:
    post = get_by_ident(y, m, d, slug)
    return post_display_func(post)
