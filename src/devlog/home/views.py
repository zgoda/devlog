from flask import render_template, current_app
from flask_login import current_user

from . import home_bp
from ..blog.service import get_recent as recent_blogs


@home_bp.route("/")
def index():
    extra_user = None
    if current_user.is_authenticated:
        extra_user = current_user
    blogs = recent_blogs(
        extra_user=extra_user, limit=current_app.config.get("SHORT_LIST_LIMIT", 5)
    )
    context = {"blogs": blogs}
    return render_template("index.jinja", **context)
