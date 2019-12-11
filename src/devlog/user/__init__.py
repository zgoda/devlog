from flask import Blueprint

user_bp = Blueprint('user', __name__)

from . import web, views  # noqa: F401,E402
