import markdown
from flask import g, request
from flask.views import MethodView

from ..models import Quip
from ..utils.pagination import get_page
from ..utils.text import PostProcessor
from . import api_bp as bp
from .schema import quip_schema
from .utils import generate_token, get_user, json_error_response, token_required


@bp.route('/login', methods=['POST', 'HEAD'])
def login():
    if request.method == 'HEAD':
        return {}
    name = request.form.get('name')
    password = request.form.get('password')
    user = get_user(name)
    if user is not None and user.check_password(password):
        g.user = user
        return {'token': generate_token(name)}
    return json_error_response(404, 'No such account')


class QuipCollection(MethodView):
    decorators = [token_required]

    def get(self):
        page = get_page()
        items = Quip.select().paginate(page, 100).order_by(Quip.created.desc())
        return {'quips': quip_schema.dump(items, many=True)}

    def post(self):
        data = quip_schema.load(request.get_json())
        quip = Quip(**data)
        quip.author = g.user.name
        quip.text_html = markdown.markdown(quip.text, **PostProcessor.MD_KWARGS)
        quip.save()
        return {'quip': quip_schema.dump(quip)}, 201


bp.add_url_rule('/quips', 'quip-collection', QuipCollection.as_view('quip_collection'))
