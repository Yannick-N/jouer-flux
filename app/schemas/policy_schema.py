from marshmallow import Schema, fields, validate

class PolicySchema(Schema):
    name = fields.String(required=True, validate=validate.Length(max=50))
    status = fields.String(validate=validate.OneOf(['active', 'inactive']))