import markdown
from flask import g, request

from ..models import Quip, User
from ..utils.pagination import get_page
from ..utils.text import PostProcessor
from . import api_bp as bp
from .schema import quip_schema
from .utils import generate_token, json_error_response, token_required


@bp.route('/login', methods=['POST'])
def login():
    name = request.form.get('name')
    password = request.form.get('password')
    user = User.get_or_none(User.name == name)
    if user is not None and user.check_password(password):
        return {'token': generate_token(name)}
    return json_error_response(404, 'No such account')


@bp.route('/quips', endpoint='quip-collection', methods=['GET', 'POST'])
@token_required
def quip_collection():
    if request.method == 'GET':
        page = get_page()
        items = Quip.select().paginate(page, 100).order_by(Quip.created.desc())
        return {'quips': quip_schema.dump(items, many=True)}
    data = quip_schema.load(request.get_json())
    quip = Quip(**data)
    quip.author = g.user.name
    quip.text_html = markdown.markdown(quip.text, **PostProcessor.MD_KWARGS)
    quip.save()
    return {'quip': quip_schema.dump(quip)}, 201
