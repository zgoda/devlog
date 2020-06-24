from flask import render_template, Blueprint

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
    return render_template('blog/post.html')
