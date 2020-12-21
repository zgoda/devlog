from flask import Blueprint

activitypub_bp = Blueprint('ap', __name__)

from . import common  # noqa: F401,E402
