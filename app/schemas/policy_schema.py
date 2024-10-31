from marshmallow import Schema, fields, validate

class PolicySchema(Schema):
    name = fields.String(required=True, validate=validate.Length(max=50))
    firewall_id = fields.Int(required=True)
    status = fields.String(validate=validate.OneOf(['active', 'inactive']))