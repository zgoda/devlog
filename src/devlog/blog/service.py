from typing import Optional

from flask_sqlalchemy import BaseQuery

from ..ext import db
from ..models import Blog


def get_recent(active_only: bool = True, limit: Optional[int] = None) -> BaseQuery:
    query = Blog.query
    if active_only:
        query = query.filter_by(active=True)
    query = query.order_by(db.desc(Blog.updated))
    if limit is not None:
        query = query.limit(limit)
    return query


def get_default() -> Optional[Blog]:
    return Blog.query.filter_by(default=True).first()
