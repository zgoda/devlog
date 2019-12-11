from flask import Blueprint

post_bp = Blueprint('post', __name__)

from . import views  # noqa: F401,E402
