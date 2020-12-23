from flask import Blueprint

activitypub_bp = Blueprint('ap', __name__, template_folder='templates')

from . import common, web  # noqa: F401,E402
