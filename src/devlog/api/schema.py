from marshmallow import Schema, fields


class QuipSchema(Schema):
    pk = fields.Integer(dump_only=True)
    author = fields.String()
    title = fields.String()
    text = fields.String(required=True)
    text_html = fields.String(dump_only=True, data_key='textHtml')
    created = fields.DateTime(dump_only=True)


quip_schema = QuipSchema()
