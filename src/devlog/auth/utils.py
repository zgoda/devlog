from flask import session
from flask_login import login_user

from ..models import User


def login_success(user: User):
    login_user(user)
    session.permanent = True
