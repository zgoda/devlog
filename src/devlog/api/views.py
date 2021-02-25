from typing import Mapping, Tuple, Union

import markdown
from flask import Response, g, request, url_for
from flask.views import MethodView

from ..models import Quip
from ..utils.pagination import get_page
from ..utils.text import PostProcessor
from . import api_bp as bp
from .schema import quip_schema
from .utils import generate_token, get_user, json_error_response, token_required


@bp.route('/login', methods=['POST', 'HEAD'])
def login() -> Union[Response, Mapping[str, str]]:
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

    def get(self) -> Mapping[str, dict]:
        page = get_page()
        items = Quip.select().paginate(page, 100).order_by(Quip.created.desc())
        return {'quips': quip_schema.dump(items, many=True)}

    def post(self) -> Tuple:
        data = quip_schema.load(request.get_json())
        quip = Quip(**data)
        if not quip.author:
            quip.author = g.user.name
        quip.text_html = markdown.markdown(quip.text, **PostProcessor.MD_KWARGS)
        quip.save()
        headers = {
            'Location': url_for('api.quip-item', quip_id=quip.pk, _external=True)
        }
        return {'quip': quip_schema.dump(quip)}, 201, headers


bp.add_url_rule('/quips', 'quip-collection', QuipCollection.as_view('quip_collection'))


class QuipItem(MethodView):
    decorators = [token_required]

    def get(self, quip_id: int) -> Union[Response, Mapping[str, dict]]:
        quip = Quip.get_or_none(Quip.pk == quip_id)
        if quip is None:
            return json_error_response(404, 'No such object')
        return {'quip': quip_schema.dump(quip)}

    def put(self, quip_id: int) -> Union[Response, Mapping[str, dict]]:
        quip = Quip.get_or_none(Quip.pk == quip_id)
        if quip is None:
            return json_error_response(404, 'No such object')
        data = quip_schema.load(request.get_json())
        for k, v in data.items():
            setattr(quip, k, v)
        quip.text_html = markdown.markdown(quip.text, **PostProcessor.MD_KWARGS)
        quip.save()
        return {'quip': quip_schema.dump(quip)}


bp.add_url_rule('/quip/<int:quip_id>', 'quip-item', QuipItem.as_view('quip_item'))
