from flask import Blueprint, abort, render_template

from .models import Post

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    posts = (
        Post.select()
        .where(Post.published.is_null(False))
        .order_by(Post.published.desc())
        .limit(5)
    )
    return render_template('index.html', posts=posts)


@bp.route('/<int:y>/<int:m>/<int:d>/<slug>')
def post(y, m, d, slug):
    post = Post.get_or_none(
        Post.c_year == y,
        Post.c_month == m,
        Post.c_day == d,
        Post.slug == slug,
        Post.published.is_null(False),
    )
    if post is None:
        abort(404)
    return render_template('blog/post.html', post=post)
