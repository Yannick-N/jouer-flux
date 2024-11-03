from marshmallow import Schema, fields, validate

class UserSchema(Schema):
    email = fields.String(required=True, validate=validate.Email())
    password = fields.String(required=True, validate=validate.Length(min=6))
    roles = fields.List(fields.String(), missing=["user"])