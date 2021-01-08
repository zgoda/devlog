from marshmallow import Schema, fields


class QuipSchema(Schema):
    pk = fields.Integer(dump_only=True)
    author = fields.String(dump_only=True)
    title = fields.String()
    text = fields.String(required=True)
    text_html = fields.String(dump_only=True)
    created = fields.DateTime(dump_only=True)


quip_schema = QuipSchema()
