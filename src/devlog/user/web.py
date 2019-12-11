from typing import Mapping

from flask_sqlalchemy import BaseQuery

from . import user_bp
from .service import user_recent_blogs, user_recent_posts


@user_bp.context_processor
def user_objects() -> Mapping[str, BaseQuery]:
    return {
        'recent_blogs': user_recent_blogs().limit(10),
        'recent_posts': user_recent_posts().limit(10),
    }
