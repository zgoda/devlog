from ..ext import db
from ..models import Blog, Post


def get_recent(public_only=True, extra_user=None, limit=None):
    query = Post.query
    if public_only:
        query = query.join(Blog).filter(Blog.public.is_(True), Post.public.is_(True))
    else:
        query = query.join(Blog).filter(
            db.or_(
                db.and_(Blog.public.is_(True), Post.public.is_(True)),
                Post.blog.user == extra_user,
            )
        )
    query = query.order_by(db.desc(Post.updated))
    if limit is not None:
        query = query.limit(limit)
    return query
