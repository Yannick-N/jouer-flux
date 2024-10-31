from marshmallow import Schema, fields

class FirewallSchema(Schema):
    name = fields.String(required=True)
    description = fields.String()
    ip_address = fields.String(required=True)