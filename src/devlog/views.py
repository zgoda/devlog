from flask import Blueprint, abort, render_template

from .ext import cache, pages
from .models import Link, Post, Quip, Tag, TaggedPost
from .utils.pagination import Pagination

bp = Blueprint('main', __name__)


@bp.context_processor
def extra_context():
    return {
        'quips': Quip.select().order_by(Quip.created.desc()).limit(3)
    }


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
@cache.cached(timeout=48*60*60, key_prefix='page:%s')
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
def post(y: int, m: int, d: int, slug: str):
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


@bp.route('/plotki')
def quips():
    query = Quip.select().order_by(Quip.created.desc())
    return render_template(
        'blog/quips.html', pagination=Pagination(query, page_size=30)
    )


@bp.route('/tag/<slug>')
def tag(slug: str):
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


@bp.route('/linki')
@cache.cached(timeout=48*60*60, key_prefix='links:%s')
def links():
    links = {}
    q = (
        Link.select(Link.section, Link.text_html)
        .order_by(Link.section, Link.pk)
    )
    for link in q:
        sect = links.setdefault(link.section, [])
        sect.append(link.text_html)
    return render_template('misc/links.html', links=links)
