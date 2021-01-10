import functools
import hashlib

from flask import Response, current_app, g, make_response, request
from itsdangerous.exc import BadSignature, SignatureExpired
from itsdangerous.url_safe import URLSafeTimedSerializer

from ..models import User


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


def token_required(func):
    @functools.wraps(func)
    def decorated_view(*args, **kw):
        auth = request.headers.get('Authorization')
        if not auth:
            return json_error_response(401, 'Authorization required')
        auth_type, auth_token = auth.split()
        if auth_type.lower() != 'basic':
            return json_error_response(400, 'Invalid authentication type')
        signer_kw = {'digest_method': hashlib.sha512}
        serializer = URLSafeTimedSerializer(
            current_app.secret_key, salt=current_app.config['TOKEN_SALT'],
            signer_kwargs=signer_kw,
        )
        try:
            name = serializer.loads(auth_token, current_app.config['TOKEN_MAX_AGE'])
            user = User.get_or_none(User.name == name)
            if not user:
                return json_error_response(400, 'Invalid token')
            g.user = user
            return func(*args, **kw)
        except SignatureExpired:
            return json_error_response(400, 'Token expired')
        except BadSignature:
            return json_error_response(400, 'Invalid token')
    return decorated_view
