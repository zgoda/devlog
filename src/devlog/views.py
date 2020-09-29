from flask import Blueprint, abort, render_template

from .ext import pages
from .models import Post, Tag, TaggedPost
from .utils.pagination import Pagination

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


@bp.route('/strona/<path:path>')
def page(path):
    page = pages.get_or_404(path)
    template = page.meta.get('template', 'flatpage.html')
    return render_template(template, page=page)


@bp.route('/blog')
def blog():
    query = (
        Post.select()
        .where(Post.published.is_null(False))
        .order_by(Post.created.desc())
    )
    return render_template('blog/home.html', pagination=Pagination(query))


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


@bp.route('/tag/<slug>')
def tag(slug):
    tag = Tag.get_or_none(Tag.slug == slug)
    if tag is None:
        abort(404)
    query = (
        Post.select()
        .join(TaggedPost)
        .where((Post.published.is_null(False)) & (TaggedPost.tag == tag))
        .order_by(Post.created.desc())
    )
    return render_template('blog/tag.html', tag=tag, pagination=Pagination(query))
