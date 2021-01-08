import hashlib

from flask import Response, current_app, make_response
from itsdangerous.url_safe import URLSafeTimedSerializer


def json_error_response(code: int, message: str) -> Response:
    """Generate Flask response with error description.

    :param code: HTTP status code
    :type code: int
    :param message: error description
    :type message: str
    :return: Flask response object
    :rtype: Response
    """
    body = {'message': message}
    return make_response(body, code)


def generate_token(payload: str) -> str:
    """Generate token for authenticating and autorising client.

    The token is URL-safe and includes timestamp.

    :param payload: data to be serialised
    :type payload: str
    :return: token string
    :rtype: str
    """
    signer_kw = {'digest_method': hashlib.sha512}
    serializer = URLSafeTimedSerializer(
        current_app.secret_key, salt=current_app.config['TOKEN_SALT'],
        signer_kwargs=signer_kw,
    )
    return serializer.dumps(payload)
