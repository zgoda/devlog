from typing import Optional

from flask_sqlalchemy import BaseQuery

from ..ext import db
from ..models import Blog, Post


def get_recent(
            active_only: bool = True, limit: Optional[int] = None,
            blog: Optional[Blog] = None,
        ) -> BaseQuery:
    query = Post.query.join(Blog)
    if blog is not None:
        query = query.filter(Post.blog == blog)
    if active_only:
        query = query.filter(Post.draft.is_(False))
    query = query.order_by(db.desc(Post.updated))
    if limit is not None:
        query = query.limit(limit)
    return query


def get_by_ident(year: int, month: int, day: int, slug: str) -> Post:
    """Get post by display ident (year, month, day and slug). Raises 404
    if not found.

    :param year: post year
    :type year: int
    :param month: post month
    :type month: int
    :param day: post day
    :type day: int
    :param slug: post slug
    :type slug: str
    :return: post instance
    :rtype: Post
    """
    return Post.query.filter(
        db.func.extract('year', Post.created) == year,
        db.func.extract('month', Post.created) == month,
        db.func.extract('day', Post.created) == day,
        Post.slug == slug,
    ).first_or_404()
