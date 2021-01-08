import hashlib

from flask import Response, current_app, make_response
from itsdangerous.url_safe import URLSafeTimedSerializer


def json_error_response(code: int, message: str) -> Response:
    body = {'message': message}
    return make_response(body, code)


def generate_token(payload: str) -> str:
    signer_kw = {'digest_method': hashlib.sha512}
    serializer = URLSafeTimedSerializer(current_app.secret_key, signer_kwargs=signer_kw)
    return serializer.dumps(payload)
