import pytz
from marshmallow import Schema, fields, pre_dump


class QuipSchema(Schema):
    pk = fields.Integer(dump_only=True)
    author = fields.String()
    title = fields.String()
    text = fields.String(required=True)
    text_html = fields.String(dump_only=True, data_key='textHtml')
    created = fields.DateTime(dump_only=True)

    @pre_dump
    def created_to_utc(self, obj, **kw):
        obj.created = pytz.utc.localize(obj.created)
        return obj


quip_schema = QuipSchema()
