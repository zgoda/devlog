from typing import Optional

from flask_sqlalchemy import BaseQuery

from ..ext import db
from ..models import Blog, User


def get_recent(
            public_only: bool = True, extra_user: Optional[User] = None,
            limit: Optional[int] = None,
        ) -> BaseQuery:
    query = Blog.query
    if public_only:
        if extra_user is None:
            query = query.filter_by(public=True)
        else:
            query = query.filter(
                db.or_(Blog.public.is_(True), Blog.user == extra_user)
            )
    query = query.order_by(db.desc(Blog.updated))
    if limit is not None:
        query = query.limit(limit)
    return query
