from flask import Blueprint

user_bp = Blueprint('user', __name__, template_folder='templates')

from . import views  # noqa: F401,E402
