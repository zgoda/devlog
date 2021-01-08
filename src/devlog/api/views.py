from flask import request

from ..models import Quip, User
from . import api_bp as bp
from .utils import generate_token, json_error_response, token_required
from .schema import quip_schema


@bp.route('/login', methods=['POST'])
def login():
    name = request.form.get('name')
    password = request.form.get('password')
    user = User.get_or_none(User.name == name)
    if user is not None and user.check_password(password):
        return {'token': generate_token(name)}
    return json_error_response(404, 'No such account')


@bp.route('/quips', endpoint='quip-collection-get')
@token_required
def get_list():
    items = Quip.select().order_by(Quip.created.desc())
    return {'quips': quip_schema.dump(items, many=True)}
