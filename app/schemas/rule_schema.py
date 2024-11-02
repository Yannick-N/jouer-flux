from marshmallow import Schema, fields

class RuleSchema(Schema):
    protocol = fields.String(required=True)
    destination_ip = fields.String(allow_none=True)