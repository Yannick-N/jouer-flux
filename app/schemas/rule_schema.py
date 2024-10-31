from marshmallow import Schema, fields

class RuleSchema(Schema):
    policy_id = fields.Integer(required=True)
    protocol = fields.String(required=True)
    destination_ip = fields.String(allow_none=True)