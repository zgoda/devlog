from ..ext import db
from ..models import Blog, Post


def get_recent(public_only=True, extra_user=None, limit=None, drafts=False, blog=None):
    query = Post.query.join(Blog)
    if blog is not None:
        query = query.filter(Post.blog == blog)
    if not drafts:
        query = query.filter(Post.draft.is_(False))
    if public_only:
        if extra_user is None:
            query = query.filter(
                db.and_(Blog.public.is_(True), Post.public.is_(True))
            )
        else:
            query = query.filter(
                db.or_(
                    db.and_(Blog.public.is_(True), Post.public.is_(True)),
                    Blog.user == extra_user,
                )
            )
    query = query.order_by(db.desc(Post.updated))
    if limit is not None:
        query = query.limit(limit)
    return query
