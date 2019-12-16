from typing import Optional

from flask_sqlalchemy import BaseQuery

from ..ext import db
from ..models import Blog, Post, User


def get_recent(
            public_only: bool = True, extra_user: Optional[User] = None,
            limit: Optional[int] = None, drafts: bool = False,
            blog: Optional[Blog] = None,
        ) -> BaseQuery:
    """Build query returning recent posts.

    :param public_only: whether only public posts to be included,
                        defaults to True
    :type public_only: bool, optional
    :param extra_user: if non-public posts or drafts have been requested this
                       is the author of the posts to be included,
                       defaults to None
    :type extra_user: Optional[User], optional
    :param limit: limit to be applied to query, defaults to None
    :type limit: Optional[int], optional
    :param drafts: whether to include drafts, defaults to False
    :type drafts: bool, optional
    :param blog: limit posts to particular blog, defaults to None
    :type blog: Optional[Blog], optional
    :return: query over posts
    :rtype: BaseQuery
    """
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
