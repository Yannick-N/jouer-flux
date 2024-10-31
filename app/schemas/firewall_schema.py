from marshmallow import Schema, fields

class FirewallSchema(Schema):
    name = fields.String(required=True)
    description = fields.String(missing="")
    ip_address = fields.String(required=True)