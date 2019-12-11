from typing import Optional

from flask_sqlalchemy import BaseQuery

from ..ext import db
from ..models import Blog, Post, User


def get_recent(
            public_only: bool = True, extra_user: Optional[User] = None,
            limit: Optional[int] = None, drafts: bool = False,
            blog: Optional[Blog] = None,
        ) -> BaseQuery:
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
