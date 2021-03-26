from typing import Any

import markupsafe
import pytz
from marshmallow import Schema, fields, post_load, pre_dump


class QuipSchema(Schema):
    pk = fields.Integer(dump_only=True)
    author = fields.String()
    title = fields.String()
    text = fields.String(required=True)
    text_html = fields.String(dump_only=True, data_key='textHtml')
    created = fields.DateTime(dump_only=True)

    @pre_dump
    def created_to_utc(self, obj: Any, **kw) -> Any:
        obj.created = pytz.utc.localize(obj.created)
        return obj

    @post_load
    def sanitise_text(self, data: dict, **kw) -> dict:
        data['text'] = markupsafe.escape_silent(data['text'])
        return data


quip_schema = QuipSchema()
