from flask_login import current_user
from flask_sqlalchemy import BaseQuery

from ..blog.service import get_recent as recent_blogs
from ..models import Blog
from ..post.service import get_recent as recent_posts


def user_recent_blogs() -> BaseQuery:
    query = recent_blogs(public_only=False)
    query = query.filter(Blog.user == current_user)
    return query


def user_recent_posts() -> BaseQuery:
    query = recent_posts(public_only=False, drafts=True)
    query = query.filter(Blog.user == current_user)
    return query
