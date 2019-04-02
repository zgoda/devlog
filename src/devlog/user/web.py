from flask_login import current_user

from . import user_bp
from .service import user_recent_blogs, user_recent_posts


@user_bp.context_processor
def user_objects():
    if current_user.is_authenticated:
        return {
            'recent_blogs': user_recent_blogs().limit(10),
            'recent_posts': user_recent_posts().limit(10),
        }
    return {
        'recent_blogs': None,
        'recent_posts': None,
    }
