from typing import Tuple

from flask import current_app
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer


def generate_token(email: str) -> str:
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=current_app.config['EMAIL_CONFIRMATION_SALT'])


def check_token(token: str) -> Tuple[bool, str]:
    result = False, 'unknown'
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token, salt=current_app.config['EMAIL_CONFIRMATION_SALT'],
            max_age=current_app.config['CONFIRMATION_TOKEN_MAX_AGE'],
        )
        result = True, email
    except SignatureExpired:
        result = False, 'expired'
    except BadSignature:
        result = False, 'invalid'
    return result
