import math

from flask import Blueprint, abort, render_template

from .models import Post, Tag
from .utils.pagination import get_page

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    posts = (
        Post.select()
        .where(Post.published.is_null(False))
        .order_by(Post.created.desc())
        .limit(5)
    )
    return render_template('index.html', posts=posts)


@bp.route('/blog')
def blog():
    page_size = 10
    page = get_page()
    post_count = (
        Post.select()
        .where(Post.published.is_null(False))
        .count()
    )
    num_pages = math.ceil(post_count / page_size)
    posts = (
        Post.select()
        .where(Post.published.is_null(False))
        .order_by(Post.created.desc())
        .paginate(page, page_size)
    )
    ctx = {
        'num_pages': num_pages,
        'page': page,
        'posts': posts,
    }
    return render_template('blog/home.html', **ctx)


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
    tags = post.tags(order=Tag.name)
    return render_template('blog/post.html', post=post, tags=tags)
